from os import urandom
from flask import Flask, abort, request, Response
from .ca import CertificateAuthority, ca_from_storage, get_ca
from base64 import b64decode
from cryptography.hazmat.primitives.serialization import Encoding
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from .message import SCEPMessage

FORCE_DEGENERATE_FOR_SINGLE_CERT = False
CACAPS = ('POSTPKIOperation', 'SHA-256', 'AES')

app = Flask(__name__)
app.config.from_object('scep.default_settings')
app.config.from_envvar('SCEP_SETTINGS')

ca = ca_from_storage(app.config['CA_ROOT'])

@app.route('/cgi-bin/pkiclient.exe', methods=['GET', 'POST'])
@app.route('/scep', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def scep():
    op = request.args.get('operation')
    mdm_ca = get_ca()

    if op == 'GetCACert':
        certs = [mdm_ca.certificate]

        if len(certs) == 1 and not FORCE_DEGENERATE_FOR_SINGLE_CERT:
            return Response(certs[0].public_bytes(Encoding.DER), mimetype='application/x-x509-ca-cert')
        elif len(certs):
            raise ValueError('cryptography cannot produce degenerate pkcs7 certs')
            # p7_degenerate = degenerate_pkcs7_der(certs)
            # return Response(p7_degenerate, mimetype='application/x-x509-ca-ra-cert')
    elif op == 'GetCACaps':
        return '\n'.join(CACAPS)
    elif op == 'PKIOperation':
        if request.method == 'GET':
            msg = request.args.get('message')
            # note: OS X improperly encodes the base64 query param by not
            # encoding spaces as %2B and instead leaving them as +'s
            msg = b64decode(msg.replace(' ', '+'))
        elif request.method == 'POST':
            # workaround for Flask/Werkzeug lack of chunked handling
            if 'chunked' in request.headers.get('Transfer-Encoding', ''):
                msg = request.environ['body_copy']
            else:
                msg = request.data

        pki_msg = SCEPMessage.from_pkcs7_der(msg)

        if pki_msg.message_type == 'pkcs_req':
            app.logger.debug('received PKCSReq SCEP message')

            cakey = mdm_ca.private_key
            cacert = mdm_ca.certificate

            der_req = pki_msg.get_decrypted_envelope_data(
                cacert,
                cakey)

            cert_req = x509.load_der_x509_csr(der_req, backend=default_backend())

            rpl_msg = CertRep()
            rpl_msg.transaction_id = pki_msg.transaction_id
            rpl_msg.recipient_nonce = pki_msg.sender_nonce
            rpl_msg.sender_nonce = urandom(16)

            rpl_msg.signing_cert = m2_x509_cacert
            rpl_msg.signing_pkey = m2_evp_cakey

            if get_challenge_password(cert_req._m2_req()) != scep_config.challenge:
                current_app.logger.error('failed challenge')

                rpl_msg.pki_status = PKI_STATUS_FAILURE

                return Response(rpl_msg.to_pkcs7_der(), mimetype='application/x-pki-message')

            # sign request and save to DB
            new_cert, db_new_cert = mdm_ca.sign_new_device_req(cert_req)

            new_cert_degen = degenerate_pkcs7_der([new_cert._m2_x509()])
            rpl_msg.signedcontent = new_cert_degen

            rpl_msg.encrypt_envelope_data(pki_msg.signing_cert)

            rpl_msg.pki_status = PKI_STATUS_SUCCESS

            return Response(rpl_msg.to_pkcs7_der(), mimetype='application/x-pki-message')
        else:
            app.logger.error('unhandled SCEP message type: %d', pki_msg.message_type)
            return ''
    else:
        abort(404, 'unknown SCEP operation')

