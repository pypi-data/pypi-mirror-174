import Form from "../../FormView/form";
import "./HeaderForm.scss";
import Swal from "sweetalert2";
import axios from "axios";
import {SERVICE_API_ADDR} from "../../../libs/constant";
import {LinearProgress} from "@material-ui/core";

class HeaderForm extends Form {
    constructor(props) {
        super(props);
        this.state = {
            data: {
                heading: "",
                sub_heading: "",
                image: File | null,
                // image_type: "Logo"
            },
            isLoading: false,
            progress: 0,
            elementId: null,
        }
    }

    static displayName = 'HeaderForm';

    componentWillReceiveProps(nextProps, nextContext) {
        this.setState({elementId: nextProps.elementId});
    }

    componentDidMount() {
    }

    // Set up the handler
    handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        this.state.data.image = event.target.files ? event.target.files[0] : null;
    };

    doSubmit = async () => {
        if (this.formValidation()) {
            console.log(this.state.data);
            // const search = this.props.location.search;
            // const projectId = new URLSearchParams(search).get("projectId");
            const formData = new FormData();
            formData.append("heading", this.state.data.heading);
            formData.append("sub_heading", this.state.data.sub_heading);
            formData.append("image_type", this.state.data.image_type);
            this.state.data.image && formData.append("image", this.state.data.image);
            return await this.dataPostAPI(`${SERVICE_API_ADDR}scenes/create/`, formData);
        } else {
            Swal.fire({
                position: 'top-end',
                icon: 'error',
                title: 'Some fields are missing ..',
                showConfirmButton: false,
                timer: 1500
            })
        }
    };

    dataPostAPI = async (url, formData) => {
        const token = JSON.parse(localStorage.getItem('token'));
        await axios.post(url, formData, {
            headers: {
                "Content-Type": "multipart/form-data",
                "x-access-token": "Bearer " + token.token
            },
            onUploadProgress: (progressEvent) => {
                const progress = (progressEvent.loaded / progressEvent.total) * 50;
                this.setState({progress: progress});
            },
            onDownloadProgress: (progressEvent) => {
                const progress = 50 + (progressEvent.loaded / progressEvent.total) * 50;
                console.log(progress);
                this.setState({progress: progress});
            },
        }).then((response) => {
            Swal.fire({
                position: 'top-end',
                icon: 'success',
                title: response.data.message,
                showConfirmButton: false,
                timer: 1500
            })
        }).catch((error) => {
            // Error
            if (error.response) {
                // The request was made and the server responded with a status code
                // that falls out of the range of 2xx
                console.log(error.response.data.message);
                Swal.fire({
                    position: 'top-end',
                    icon: 'error',
                    title: error.response.data.message,
                    showConfirmButton: false,
                    timer: 1500
                })
                // console.log(error.response.status);
                // console.log(error.response.headers);
            } else if (error.request) {
                // The request was made but no response was received
                // `error.request` is an instance of XMLHttpRequest in the
                // browser and an instance of
                // http.ClientRequest in node.js
                console.log(error.request);
            } else {
                // Something happened in setting up the request that triggered an Error
                console.log('Error', error.message);
            }
            console.log(error.config);
        });
    }

    formValidation() {
        return this.state.data.heading !== '' && this.state.data.sub_heading !== '' && this.state.data.image !== 0;
    }

    render() {
        return (
            <div ref={headerForm => this.headerForm = headerForm} className="headerFom-view">
                <form onSubmit={this.handleSubmit} id="customCardForm" noValidate>
                    <h5>Title/Heading Information</h5>
                    <p></p>
                    {this.renderTextInput("heading", "Heading", "text", true)}
                    {this.renderTextInput("sub_heading", "Sub Heading", "text", false)}
                    <p></p>
                    <h5>Logo/Banner Information</h5>
                    <p></p>
                    <div className="fileUpload">
                        <label>Upload Scene Stylesheet(Only CSS type)</label>
                        <p></p>
                        <input type="file" name="stylesheet" onChange={this.handleImageChange} required="required"/>
                    </div>
                    {this.renderRadioInput("image_type", "Mark Image as", ['Logo', 'Banner'], true)}
                    {this.renderSubmitBtn("Submit")}
                </form>
                <LinearProgress variant="determinate" value={this.state.progress}/>
            </div>
        );
    }

}

export default HeaderForm;