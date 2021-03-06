import * as React from 'react';
import {connect, Dispatch} from 'react-redux';
import {RouteComponentProps} from 'react-router';
import {RootState} from "../../reducers/index";
import {bindActionCreators} from "redux";
import {CertificatesActionRequest, certificates as fetchInstalledCertificates} from "../../actions/device/certificates";
import {InstalledCertificatesState} from "../../reducers/device/installed_certificates";
import Griddle, {RowDefinition, ColumnDefinition} from 'griddle-react';
import {SemanticUIPlugin} from "../../griddle-plugins/semantic-ui/index";
import {SimpleLayout as Layout} from "../../components/griddle/SimpleLayout";
import {CertificateTypeIcon} from "../../components/CertificateTypeIcon";
import {griddle, GriddleDecoratorState} from "../../hoc/griddle";
import {CertificateRow} from "../../components/griddle/CertificateRow";
import {ListTableBody, ListTableContainer} from "../../components/griddle/ListTable";

interface ReduxStateProps {
    installed_certificates: InstalledCertificatesState;
}

function mapStateToProps(state: RootState, ownProps?: any): ReduxStateProps {
    return {
        installed_certificates: state.device.installed_certificates
    }
}

interface ReduxDispatchProps {
    fetchInstalledCertificates: CertificatesActionRequest;
}

function mapDispatchToProps(dispatch: Dispatch<any>): ReduxDispatchProps {
    return bindActionCreators({
        fetchInstalledCertificates
    }, dispatch);
}

interface DeviceCertificatesRouteProps {
    id: string; // device id
}

interface DeviceCertificatesProps extends ReduxStateProps, ReduxDispatchProps, RouteComponentProps<DeviceCertificatesRouteProps> {
    griddleState: GriddleDecoratorState;
    events: any;
}

interface DeviceCertificatesState {
}


export class UnconnectedDeviceCertificates extends React.Component<DeviceCertificatesProps, any> {

    componentWillMount?() {
        this.props.fetchInstalledCertificates(this.props.match.params.id, this.props.griddleState.pageSize);
    }

    componentWillUpdate(nextProps: DeviceCertificatesProps, nextState: DeviceCertificatesState) {
        const {griddleState} = this.props;
        const {griddleState: nextGriddleState} = nextProps;

        if (nextGriddleState.filter !== griddleState.filter || nextGriddleState.currentPage !== griddleState.currentPage) {
            this.props.fetchInstalledCertificates(
                ''+this.props.match.params.id,
                nextGriddleState.pageSize,
                nextGriddleState.currentPage, [],
                [{ name: 'x509_cn', op: 'ilike', val: `%${nextGriddleState.filter}%` }]);
        }
    }

    render(): JSX.Element {
        const {
            installed_certificates,
            griddleState
        } = this.props;

        return (
            <div className='DeviceCertificates'>
                {installed_certificates.items &&
                <Griddle
                    data={installed_certificates.items}
                    plugins={[SemanticUIPlugin()]}
                    styleConfig={{
                        classNames: {
                            Table: 'ui celled table',
                            NoResults: 'ui message'
                        }
                    }}
                    events={this.props.events}
                    components={{
                        Layout,
                        Row: CertificateRow,
                        TableContainer: ListTableContainer,
                        TableBody: ListTableBody
                    }}
                    pageProperties={{
                        currentPage: griddleState.currentPage,
                        pageSize: griddleState.pageSize,
                        recordCount: installed_certificates.recordCount
                    }}
                >
                    <RowDefinition onClickButton={(e: any) => { console.log('clicked button'); }}>
                    </RowDefinition>
                </Griddle>}
            </div>
        )
    }
}

export const DeviceCertificates = connect<ReduxStateProps, ReduxDispatchProps, DeviceCertificatesProps>(
    mapStateToProps,
    mapDispatchToProps
)(griddle(UnconnectedDeviceCertificates));
