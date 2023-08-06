import "./NewSection.scss"
import {withRouter} from "react-router-dom";
import Form from "../FormView/form";
import Swal from "sweetalert2";
import {dataProject} from "../../libs/panobase/service";
import {APP_URL_PREFIX} from "../../libs/constant";

class NewSection extends Form {
    constructor(props) {
        super(props);
        this.state = {
            projects: null
        }
        this.handleClick = this.handleClick.bind(this);
    }

    componentDidMount() {
        dataProject.getProjects().then(r => {
            this.setState({projects: r})
        });
    }

    newProjectPopup() {
        Swal.fire({
            title: 'Your Project name',
            input: 'text',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,
            confirmButtonText: 'Create',
            showLoaderOnConfirm: true,
            preConfirm: async (name) => {
                return await dataProject.createProject(name)
            },
            allowOutsideClick: () => !Swal.isLoading()
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({
                    title: `Project "${result.value}" created`,
                })
            }
        })
    }

    handleClick(project) {
        window.location.href = `${APP_URL_PREFIX}create?projectId=${project}&sceneId=default`;
    }

    getProjects() {
        let projs = []
        projs.push(this.state.projects.map((object, i) => {
            return (<div key={object} className="stacked-project miniCard new-project">
                <div style={{height: "80%"}}>
                    <img
                        src="https://www.cio.com/wp-content/uploads/2021/12/company-strategy-ts-100593661-orig.jpg?quality=50&strip=all"
                        alt={object}
                        style={{width: "100%"}}
                    />
                    <button className="btn openProject" type="button">
                        <span className="material-symbols-outlined">view_in_ar</span>
                    </button>
                </div>
                <button className="glow-on-hover" type="button" onClick={()=>this.handleClick(object)}>Add New Scene!</button>
            </div>);
        }));
        return projs
    }

    render() {
        console.log(this.state.projects);
        return (
            <div className="new-section-div">
                <div className="demo">
                    <div className="mainCard">
                        <div className="mainCardHeader"></div>
                        <div className="mainCardContent">
                            <div className="miniCard new-project">
                                <div style={{height: "80%"}}><img
                                    src="https://www.pngitem.com/pimgs/m/267-2673374_project-management-background-hd-png-download.png"
                                    alt="New Project Idea"
                                    style={{width: "100%"}}/></div>
                                <button className="glow-on-hover" type="button" onClick={this.newProjectPopup}>Create
                                    New Project!
                                </button>
                            </div>
                            {this.state.projects &&
                                this.getProjects()
                            }
                        </div>
                    </div>

                </div>
            </div>
        );
    }
}

export default withRouter(NewSection);