import {PureComponent} from "react";
import "./Navigation.scss"

class Navigation extends PureComponent {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
    }

    render() {
        return (
            <>
                <div className="NavigationComp">
                        <span><span></span></span>
                        <div className="wrap">
                            <a href="#">
                                <div></div>
                            </a>
                            <a href="#">
                                <div></div>
                            </a>
                            <a href="#">
                                <div></div>
                            </a>
                            <a href="#">
                                <div></div>
                            </a>
                            <a href="#">
                                <div></div>
                            </a>
                        </div>
                    </div>
            </>
        )
    }
}

export default Navigation;