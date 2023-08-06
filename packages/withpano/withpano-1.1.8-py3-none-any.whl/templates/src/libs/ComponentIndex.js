let Components = {};
export const REGISTER_COMPONENTS = [
    {name: 'Navigation', path: require('../components/Navigation/Navigation')},
    {name: 'SceneUpload', path:  require('../components/CreateRoom/SceneUpload')},
    {name: 'Header', path:  require('../components/DesignComp/PlainHolder/Header')}
];
REGISTER_COMPONENTS.forEach((element) => Components[element.name] = element.path.default)

export default Components;