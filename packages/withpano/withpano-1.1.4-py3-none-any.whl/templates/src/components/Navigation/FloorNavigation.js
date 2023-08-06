import {PureComponent} from "react";
import "./Navigation2.scss"

class FloorNavigation extends PureComponent {
    constructor(props) {
        super(props);
    }

    componentDidMount() {
    }

    render() {
        return (
            <>
                <div className="floorNavigation">
                    <a className='button ctrl' href='#' tabIndex='1'>★</a>
                    <ul className='tip ctrl'>
                        <li className='slice left-arrow'>
                            <div><span className="material-symbols-outlined" style={{transform: "skewY(0deg) rotate(60deg)"}}>keyboard_double_arrow_left</span></div>
                        </li>
                        <li className='slice top-arrow'>
                            <div><span className="material-symbols-outlined">pinch_zoom_out</span></div>
                        </li>
                        <li className='slice'>
                            <div>✵</div>
                        </li>
                        <li className='slice bottom-arrow'>
                            <div><span className="material-symbols-outlined">pinch_zoom_in</span></div>
                        </li>
                        <li className='slice right-arrow'>
                            <div><span className="material-symbols-outlined" style={{transform: "skewY(0deg) rotate(-60deg)"}}>keyboard_double_arrow_right</span></div>
                        </li>
                    </ul>
                </div>
            </>
        )
    }
}

export default FloorNavigation;