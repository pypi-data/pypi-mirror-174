import "./styles.scss";
import {useUploadForm} from "../../libs/panobase/uploadForm";
import {SERVICE_API_ADDR} from "../../libs/constant";
import {useState} from "react";
import {LinearProgress} from "@material-ui/core";
import Button from "@material-ui/core/Button";
import {useHistory} from "react-router-dom";
import TextInput from "../FormView/textInput";
import SelectInput from "../FormView/selectInput";


export default function SceneUpload() {
    const history = useHistory();

    const options = [
        {value: 'Standalone', label: 'Standalone'},
        {value: '360View', label: '360View'}
    ]

    const [formValues, setFormValues] = useState({
        name: "",
        face_size: "",
        type: "",
        file: File | null,
        stylesheet:File | null
    });
    const {isSuccess, uploadForm, progress} = useUploadForm(
        SERVICE_API_ADDR + 'scenes/create/'
    );

    const handleSubmit = async (e) => {
        e.preventDefault();
        const search = history.location.search;
        console.log(search);
        const projectId = new URLSearchParams(search).get("projectId");
        const formData = new FormData();
        formData.append("name", formValues.name);
        formData.append("face_size", formValues.face_size);
        formData.append("type", formValues.type);
        formData.append("project", projectId);
        formValues.file && formData.append("file", formValues.file);
        formValues.stylesheet && formData.append("stylesheet", formValues.stylesheet);
        console.log(formValues);
        return await uploadForm(formData);
    };

    // Handlers for the input
    const handleNameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormValues((prevFormValues) => ({
            ...prevFormValues,
            name: event.target.value,
        }));
    };

    const handleFaceChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormValues((prevFormValues) => ({
            ...prevFormValues,
            face_size: event.target.value,
        }));
    };

    const handleTypeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormValues((prevFormValues) => ({
            ...prevFormValues,
            type: event.target.value,
        }));
    };

    // Set up the handler
    const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormValues((prevFormValues) => ({
            ...prevFormValues,
            file: event.target.files ? event.target.files[0] : null,
        }));
    };

    // Set up the handler
    const handleStylesheetChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setFormValues((prevFormValues) => ({
            ...prevFormValues,
            stylesheet: event.target.files ? event.target.files[0] : null,
        }));
    };

    return (
        <div className="formHolder" style={{width: "22%"}}>
            <form onSubmit={handleSubmit} id="customForm" noValidate method="post">
                <h5>Information</h5>
                <p></p>
                <TextInput
                    onChange={handleNameChange}
                    value={formValues.title}
                    label="Scene name"
                    name="name"
                    required={true}
                />
                <TextInput
                    onChange={handleFaceChange}
                    value={formValues.face_size}
                    label="Face Size"
                    type="number"
                    /*min={1024}
                    step={1024}
                    max={6144}*/
                    required={true}
                    name="face_size"
                />
                <SelectInput
                    name="type"
                    value={formValues.type}
                    options={['Standalone', '360View']}
                    label="Scene Type"
                    required={true}
                    onChange={handleTypeChange}
                />
                <div className="fileUpload" style={{padding: "10px"}}>
                    <label>Upload Scene Image</label>
                    <input type="file" name="file" onChange={handleImageChange}/>
                </div>
                <div className="fileUpload" style={{padding: "10px"}}>
                    <label>Upload Scene Stylesheet(Only CSS type)</label>
                    <input type="file" name="stylesheet" onChange={handleStylesheetChange}/>
                </div>
                <Button type="submit" onClick={handleSubmit}>Submit</Button>
            </form>
            <LinearProgress variant="determinate" value={progress}/>
        </div>
    )
};