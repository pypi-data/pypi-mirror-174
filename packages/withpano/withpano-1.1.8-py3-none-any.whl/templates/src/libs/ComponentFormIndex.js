let ComponentsForm = {};
export const REGISTER_FORM_COMPONENTS = [
    {name: 'Header', path:  require('../components/DesignComp/PlainHolder/HeaderForm')}
];
REGISTER_FORM_COMPONENTS.forEach((element) => ComponentsForm[element.name] = element.path.default)

export default ComponentsForm;