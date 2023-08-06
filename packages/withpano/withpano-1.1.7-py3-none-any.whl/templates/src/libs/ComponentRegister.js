import ReactDOM from "react-dom";
import Components, {REGISTER_COMPONENTS} from "./ComponentIndex";

class ComponentRegister {
    listComponent() {
        let item = []
        REGISTER_COMPONENTS.forEach((element)=>item.push(element.name));
        return item;
    }

    renderComponent(comp, domElement, eleId=null) {
        console.log(this.listComponent());
        const ComponentToRender = Components[comp]
        ReactDOM.render(<ComponentToRender elementId={eleId}/>, domElement);
    }
}

export default ComponentRegister;