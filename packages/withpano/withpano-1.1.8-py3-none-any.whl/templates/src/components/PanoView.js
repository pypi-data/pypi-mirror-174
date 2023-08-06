import React, {PureComponent} from 'react'
import Marzipano from 'marzipano';

import './Pano.css';
import TourSettings from "../libs/TourSettings";
import {dataHotspots, dataScenes} from "../libs/panobase/service";
import {withRouter} from "react-router-dom";
import ComponentRegister from "../libs/ComponentRegister";

class PanoView extends PureComponent {
    constructor(props) {
        super(props);
        this.state = {
            show: true,
            data: null,
            ...props
        }
        this.viewLeftElement = null;
        this.viewRightElement = null;
        this.viewInElement = null;
        this.viewOutElement = null;
        /*SCENE*/
        this.scene = null;
        this.viewer = null;
    }

    static displayName = 'PanoView';


    componentDidMount() {
        this.viewLeftElement = document.querySelector('.left-arrow');
        this.viewRightElement = document.querySelector('.right-arrow');
        this.viewInElement = document.querySelector('.top-arrow');
        this.viewOutElement = document.querySelector('.bottom-arrow');

        this.loadRequestedScene(this.requestedScene(this.props)).then(r => {
            console.log("PANVIEW SCENE LOADED")
        })

    }

    requestedScene(props) {
        const search = props.location.search;
        const sceneId = new URLSearchParams(search).get("sceneId");
        const newYaw = new URLSearchParams(search).get("y");
        const newPitch = new URLSearchParams(search).get("p");
        if (sceneId) {
            return sceneId;
        } else {
            props.history.push(props.location.pathname + '?sceneId=default');
            return;
        }
    }

    async loadRequestedScene(nextScene) {
        const s = await dataScenes.getScene(nextScene);
        console.log(s);
        // You need use a URL hosted with pictures /tiles
        this.viewer = new Marzipano.Viewer(this.PanoView, {});
        const image = TourSettings.getSceneImage(s.scene_image);
        const source = Marzipano.ImageUrlSource.fromString(image);
        const limiter = Marzipano.RectilinearView.limit.traditional(s.faceSize, 100 * Math.PI / 180, 120 * Math.PI / 180);
        const view = new Marzipano.RectilinearView(s.initialViewParameters, limiter);
        const geometry = new Marzipano.EquirectGeometry(s.levels);

        // Dynamic parameters for controls.
        const velocity = 0.7;
        const friction = 3;

        // Associate view controls with elements.
        // let controls = this.viewer.controls();
        // controls.registerMethod('leftElement', new Marzipano.ElementPressControlMethod(this.viewLeftElement, 'x', -velocity, friction), true);
        // controls.registerMethod('rightElement', new Marzipano.ElementPressControlMethod(this.viewRightElement, 'x', velocity, friction), true);
        // controls.registerMethod('inElement', new Marzipano.ElementPressControlMethod(this.viewInElement, 'zoom', -velocity, friction), true);
        // controls.registerMethod('outElement', new Marzipano.ElementPressControlMethod(this.viewOutElement, 'zoom', velocity, friction), true);

        this.scene = this.viewer.createScene({
            source, geometry, view
        });
        await this.loadSceneHotspots(nextScene);
        /*LOAD SCENE*/
        this.scene.switchTo();
    }

    async loadSceneHotspots(scene) {
        const hotspots = await dataHotspots.getSceneHotspots(scene);
        hotspots.forEach((hotspot) => {
            let divHotspot = this.placeHotspotElement(hotspot.info.elementId, hotspot);
            const elePerspective = {
                radius: hotspot.info.radius || 800,
                extraTransforms: hotspot.info.extraTransforms || "rotateX(0deg)"
            }
            console.log(elePerspective);
            this.scene.hotspotContainer().createHotspot(divHotspot, hotspot.position, {
                perspective: {
                    radius: hotspot.info.radius || 800,
                    extraTransforms: hotspot.info.transform || "rotateX(0deg)"
                }
            });
        });
    }

    placeHotspotElement(eleId, hotspotData = null) {
        const componentRegister = new ComponentRegister();
        let divHotspot = document.createElement("div");
        if (eleId) {
            divHotspot.setAttribute("id", eleId);
        }
        divHotspot.classList.add("hotspot");
        if (hotspotData) {
            componentRegister.renderComponent(hotspotData.info.component, divHotspot);
        }
        return divHotspot;
    }

    render() {
        return (
            <div className="pano-container" ref={PanoView => this.PanoView = PanoView}></div>
        );
    }
};

export default withRouter(PanoView);