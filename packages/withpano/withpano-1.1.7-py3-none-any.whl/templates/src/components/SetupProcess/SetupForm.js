/*
import "./styles.scss";
import SceneUpload from "./SceneUpload";
import React from "react";
import Form from "../FormView/form";
import ComponentRegister from "../../libs/ComponentRegister";


class HotsPotProp extends Form {
    constructor(props) {
        super(props);
        this.state = {
            data: this.dataFromLocalStorage(props),
            ...props
        }
        this.componentRegister = new ComponentRegister;
    }

    componentWillReceiveProps(nextProps, nextContext) {
        const compData = this.dataFromLocalStorage(nextProps);
        this.setState({data: compData});

    }

    dataFromLocalStorage(nextProps) {
        let compData = JSON.parse(localStorage.getItem(nextProps.dataComp));
        if (compData.info) {
            return compData.info;
        } else {
            return {
                elementId: nextProps.dataComp,
                name: "Test",
                type: "",
                component: "SceneUpload",
                radius: "800",
                transform: "",
                className: ""
            }
        }
    }

// state = {};

    doSubmit = () => {
        let compData = JSON.parse(localStorage.getItem(this.state.data.elementId));
        compData['info'] = this.state.data
        localStorage.setItem(this.state.data.elementId, JSON.stringify(compData));
    };

    render() {
        return (
            <div className="formHolder" style={{width: "22%"}}>
                <form onSubmit={this.handleSubmit} id="customForm" noValidate>
                    {/!*<Card className="form">*!/}
                    <h5>Information</h5>
                    <p></p>
                    {this.renderTextInput("elementId", "Element Id")}
                    {this.renderTextInput("name", "Name")}
                    {this.renderSelectInput("type", "Type", ['Info', 'Link', 'External Link'], true)}
                    {this.renderSelectInput("component", "Component", this.componentRegister.listComponent(), true)}
                    {/!*</Card>
                    <Card className="form">*!/}
                    <h5>Style and Other Attributes</h5>
                    <p></p>
                    {this.renderTextInput("radius", "Radius", "text", false)}
                    {this.renderTextInput("transform", "Transform", "text", false)}
                    {this.renderTextInput("className", "Class Name", "text", false)}
                    {this.renderSubmitBtn("Submit")}
                    {/!*</Card>*!/}
                </form>
            </div>
        );
    }
}

export default HotsPotProp;
*/
