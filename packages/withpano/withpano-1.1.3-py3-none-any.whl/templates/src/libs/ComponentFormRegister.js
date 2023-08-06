import ReactDOM from "react-dom";
import ComponentsForm, {REGISTER_FORM_COMPONENTS} from "./ComponentFormIndex";

class ComponentFormRegister {
    listComponent() {
        let item = []
        REGISTER_FORM_COMPONENTS.forEach((element)=>item.push(element.name));
        return item;
    }

    renderComponent(comp, domElement, eleId=null) {
        console.log(this.listComponent());
        const ComponentFormRender = ComponentsForm[comp]
        ReactDOM.render(<ComponentFormRender elementId={eleId}/>, domElement);
    }
}

export default ComponentFormRegister;