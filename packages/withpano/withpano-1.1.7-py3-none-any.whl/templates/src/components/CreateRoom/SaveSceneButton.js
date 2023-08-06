import {PureComponent} from "react";
import "./SaveSceneButton.scss"

class SaveSceneButton extends PureComponent {
    constructor(props) {
        super(props);

    }

    render() {
        return (
            <div className="wrapper">
                <a href="#" data-title="Click to Save!" data-pre-title="Save Scene Info!">Save Scene Info!</a>
            </div>
        );
    }
}

export default SaveSceneButton;