import React from "react";
import {Redirect, Route, Switch, withRouter} from "react-router-dom";
import Pano from "./Pano";
import SceneUpload from "./CreateRoom/SceneUpload";
import PanoView from "./PanoView";
import NewSection from "./ProjectSelection/NewSection";

class Landing extends React.Component {

    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        const search = this.props.location.search;
        const sceneId = new URLSearchParams(search).get("sceneId");
        const pathName = this.props.location.pathname;
        return (
            <Switch>
                <Route exact path="/withpano/">
                    <NewSection/>
                </Route>
                <Route exact path="/withpano/create">
                    <div id="elementEditProp"></div>
                    <Pano/>
                    {sceneId === 'default' &&
                        <SceneUpload/>
                    }
                </Route>
                <Route exact path="/withpano/my-scene">
                    <PanoView/>
                </Route>
                <Redirect to='/withpano/'/>
            </Switch>
        );
    }
}

export default withRouter(Landing);
