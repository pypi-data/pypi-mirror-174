import React, {PureComponent} from 'react'
import ReactDOM from "react-dom";
import Marzipano from 'marzipano';

import './Pano.css';
import TourSettings from "../libs/TourSettings";
import {dataScenes} from "../libs/panobase/service";
import {withRouter} from "react-router-dom";
import HotsPotProp from "./CreateRoom/HotsPotProp";
import ComponentRegister from "../libs/ComponentRegister";
import FloorNavigation from "./Navigation/FloorNavigation";
import SaveSceneButton from "./CreateRoom/SaveSceneButton";
import Header from "./DesignComp/PlainHolder/Header";
import {APP_URL_PREFIX, SERVICE_ADDR} from "../libs/constant";
import ComponentFormRegister from "../libs/ComponentFormRegister";

class Pano extends PureComponent {
    constructor(props) {
        super(props);
        this.state = {
            show: false,
            data: null,
            navShow: true,
            sceneId: null,
            projectId: null,
            ...props
        }
        this.viewLeftElement = null;
        this.viewRightElement = null;
        this.viewInElement = null;
        this.viewOutElement = null;
        /*SCENE*/
        this.scene = null;
        this.viewer = null;
        this.submitHotspots = this.submitHotspots.bind(this);
        this.editProp = false
        this.selectedElement = null;
        this.selectedSettingsElement = null;
        this.token = JSON.parse(localStorage.getItem('token')).token;
    }

    static displayName = 'Pano';

    handleCallback = (childData) => {
        console.log("CHILDDATA", childData);
        this.editProp = childData;
    }

    handleOnEditClick() {
        this.editProp = true;
        ReactDOM.render(<HotsPotProp props={this.props} dataComp={this.selectedElement} editProp={this.editProp}
                                     scene={this.state.sceneId}/>, document.getElementById('elementEditProp'));
    }

    handleOnSettingsClick(){
        const componentFormRegister = new ComponentFormRegister();
        componentFormRegister.renderComponent(this.selectedSettingsElement, document.getElementById('elementEditProp'));
    }

    componentDidMount() {
        this.viewLeftElement = document.querySelector('.left-arrow');
        this.viewRightElement = document.querySelector('.right-arrow');
        this.viewInElement = document.querySelector('.top-arrow');
        this.viewOutElement = document.querySelector('.bottom-arrow');
        this.projectScene(this.getRequestedScene(this.props)).then(r => {
            console.log("SCENE LOADED")
        })

    }

    getRequestedScene(props) {
        const search = props.location.search;
        const sceneId = new URLSearchParams(search).get("sceneId");
        const projectId = new URLSearchParams(search).get("projectId");
        const newYaw = new URLSearchParams(search).get("y");
        const newPitch = new URLSearchParams(search).get("p");
        if (projectId) {
            if (sceneId) {
                if (sceneId === 'default') {
                    this.setState({show: false});
                } else {
                    if (localStorage.getItem(sceneId) === undefined) {
                        localStorage.setItem(sceneId, JSON.stringify({}));
                    }
                    this.setState({show: true});
                }
                this.setState({sceneId: sceneId, projectId: projectId});
                return {sceneId, projectId};
            } else {
                props.history.push(props.location.pathname + '?projectId=' + projectId + '&sceneId=default');
                return;
            }
        } else {
            window.location.href = {APP_URL_PREFIX}
            return;
        }
        // }else{
        //     return "default";
        // }
    }

    async projectScene(nextScene) {
        const s = await dataScenes.getScene(nextScene.sceneId, nextScene.projectId);
        if (s.type === '360View') {
            await this.loadScenes(nextScene, s)
        } else {
            this.setState({navShow: false})
            await this.loadStaticView(nextScene, s)
        }
        console.log(s);
    }

    /* LOAD VIEW START*/
    async loadStaticView(nextScene, s) {
        this.pano.setAttribute('style', 'position:fixed');
        this.pano.classList.add('static-view-only');
        const image = TourSettings.getSceneImage(nextScene.sceneId, nextScene.projectId);
        let staticBg = document.createElement("img");
        staticBg.src = image;
        staticBg.classList.add("static-bg-img");
        this.pano.append(staticBg);
        document.body.addEventListener("wheel", e => {
            if (e.ctrlKey)
                e.preventDefault();//prevent zoom
        });

        if (nextScene.sceneId !== 'default') {
            this.pano.addEventListener("contextmenu", (e) => {
                const eleId = Math.random() + '-ids';
                const pinCoords = {
                    x: `${(e.pageX / window.screen.width) * 100}%`,
                    y: `${(e.pageY / window.screen.height) * 100}%`
                };
                let staticBgDiv = this.createHotspotElement(eleId);
                staticBgDiv.setAttribute('style', `top: ${pinCoords.y};left: ${pinCoords.x}`)
                staticBgDiv.setAttribute('data-x', `${e.pageX}`);
                staticBgDiv.setAttribute('data-y', `${e.pageY}`);
                this.pano.append(staticBgDiv);
                this.addStaticElementDrag(staticBgDiv, staticBgDiv, this.state.sceneId);
                e.preventDefault();
            })
            await this.loadStaticHotspots(s.hotspot);
        }
    }

    async loadScenes(nextScene, s) {
        // You need use a URL hosted with pictures /tiles
        this.viewer = new Marzipano.Viewer(this.pano, {});
        const image = TourSettings.getSceneImage(nextScene.sceneId, nextScene.projectId);
        const source = Marzipano.ImageUrlSource.fromString(image);
        const limiter = Marzipano.RectilinearView.limit.traditional(s.faceSize, 100 * Math.PI / 180, 120 * Math.PI / 180);

        // const limiter2 = Marzipano.RectilinearView.limit.yaw(0,0);

        function myLimiter(params) {
            var modifiedParams = limiter(params);
            // modifiedParams = limiter2(modifiedParams);
            return modifiedParams;
        }

        const view = new Marzipano.RectilinearView(s.initialViewParameters, myLimiter);
        const geometry = new Marzipano.EquirectGeometry(s.levels);

        // Dynamic parameters for controls.
        const velocity = 0.7;
        const friction = 3;

        // Associate view controls with elements.
        let controls = this.viewer.controls();
        controls.registerMethod('leftElement', new Marzipano.ElementPressControlMethod(this.viewLeftElement, 'x', -velocity, friction), true);
        controls.registerMethod('rightElement', new Marzipano.ElementPressControlMethod(this.viewRightElement, 'x', velocity, friction), true);
        controls.registerMethod('inElement', new Marzipano.ElementPressControlMethod(this.viewInElement, 'zoom', -velocity, friction), true);
        controls.registerMethod('outElement', new Marzipano.ElementPressControlMethod(this.viewOutElement, 'zoom', velocity, friction), true);

        this.scene = this.viewer.createScene({
            source, geometry, view
        });
        this.pano.addEventListener("click", (e) => {
            const pinCoords = view.screenToCoordinates({x: e.x, y: e.y}, {x: e.x, y: e.y});
            console.log(pinCoords);
        })
        if (nextScene.sceneId !== 'default') {
            this.pano.addEventListener("contextmenu", (e) => {
                const pinCoords = view.screenToCoordinates({x: e.x, y: e.y}, {x: e.x, y: e.y});
                this.addHotspots(pinCoords);
                console.log(pinCoords);
                e.preventDefault();
            })
            await this.loadHotspots(s.hotspot);
        }
        /*LOAD SCENE*/
        this.scene.switchTo();
    }

    /* LOAD VIEW END*/

    addHotspots(coords) {
        let divHotspot = this.createHotspotElement(Math.random() + '-ids');
        divHotspot.addEventListener("click", (e) => {
            this.selectedElement = e.currentTarget.id;
            this.handleOnEditClick();
        })
        const createdHotspot = this.scene.hotspotContainer().createHotspot(divHotspot, coords, {
            perspective: {
                //radius: 0 || 800,
                //extraTransforms: "" || "rotateX(0deg)"
            }
        });
        this.addDrag(divHotspot, createdHotspot, this.state.sceneId);
    }

    allLocalStorageRecord() {
        let archive = [], // Notice change here
            records = JSON.parse(localStorage.getItem(this.state.sceneId));
        if (records) {
            for (const [key, value] of Object.entries(records)) {
                if (value.info) {
                    archive.push(value);
                } else {
                    delete records[key];
                }
            }
        }
        localStorage.setItem(this.state.sceneId, JSON.stringify(records));
        return archive;
    }

    async loadHotspots(savedHotspot = null) {
        // dataScenes.cleanStorage();
        this.allLocalStorageRecord().forEach((hotspot) => {
            let divHotspot = this.createHotspotElement(hotspot.info.elementId, hotspot);
            const elePerspective = {
                radius: hotspot.info.radius || 800,
                extraTransforms: hotspot.info.extraTransforms || "rotateX(0deg)"
            }
            console.log(elePerspective);
            const createdHotspot = this.scene.hotspotContainer().createHotspot(divHotspot, hotspot.position, {
                perspective: {
                    radius: hotspot.info.radius || 800,
                    extraTransforms: hotspot.info.transform || "rotateX(0deg)"
                }
            });

            this.addDrag(divHotspot, createdHotspot, this.state.sceneId);
        });
    }

    async loadStaticHotspots(savedHotspot = null) {
        this.allLocalStorageRecord().forEach((hotspot) => {
            console.log(hotspot);
            let divHotspot = this.createHotspotElement(hotspot.info.elementId, hotspot);
            divHotspot.setAttribute('style', `top: ${hotspot.position.top}%;left: ${hotspot.position.left}%;transform: ${hotspot.info.transform} translateX(${hotspot.position.x}px) translateY(${hotspot.position.y}px) translateZ(0px)`)
            divHotspot.setAttribute('data-x', `${hotspot.position.x}`);
            divHotspot.setAttribute('data-y', `${hotspot.position.y}`);
            this.pano.append(divHotspot);
            this.addStaticElementDrag(divHotspot, divHotspot, this.state.sceneId);
        });
    }

    createHotspotElement(eleId, hotspotData = null) {
        const componentRegister = new ComponentRegister();
        let divHotspot = document.createElement("div");
        if (eleId) {
            divHotspot.setAttribute("id", eleId);
        }
        divHotspot.classList.add("hotspot");
        if (hotspotData) {
            componentRegister.renderComponent(hotspotData.info.component, divHotspot, eleId);
            let settingsMenu = document.createElement("span");
            settingsMenu.classList.add("material-symbols-outlined");
            settingsMenu.innerText = "settings";
            settingsMenu.addEventListener("click", (e) => {
                this.selectedSettingsElement = hotspotData.info.component;
                this.handleOnSettingsClick();
            })
            divHotspot.appendChild(settingsMenu);
        } else {
            let divHotspotOut = document.createElement("div");
            divHotspotOut.classList.add("out");
            let divHotspotIn = document.createElement("div");
            divHotspotIn.classList.add("in");
            let imgHotspot = document.createElement("img");
            imgHotspot.classList.add("hotspot-icon");
            imgHotspot.src = TourSettings.getHotspotImage("info");
            divHotspotIn.appendChild(imgHotspot);
            divHotspot.appendChild(divHotspotOut);
            divHotspot.appendChild(divHotspotIn);
        }
        /*EDIT HOTSPOT*/
        let editHotspot = document.createElement("span");
        editHotspot.classList.add("material-symbols-outlined");
        editHotspot.innerText = "edit_note";
        divHotspot.setAttribute("data-id", eleId);
        editHotspot.addEventListener("click", (e) => {
            this.selectedElement = eleId;
            this.handleOnEditClick();
        })
        divHotspot.appendChild(editHotspot);
        return divHotspot;
    }

    /* ELEMENT DRAG*/
    addDrag(element, hotspot, sceneId) {
        let lastX, lastY;
        let viewer = this.viewer;

        function onMouseDown(event) {
            lastX = event.x;
            lastY = event.y;

            viewer.controls().disable();

            window.addEventListener("mousemove", onMouseMove);
            window.addEventListener("mouseup", onMouseUp);
        }

        function onMouseMove(event) {
            const x = event.x;
            const y = event.y;

            const pinCoords = viewer.view().screenToCoordinates({x: x, y: y});
            console.log("CORDS", pinCoords);
            hotspot.setPosition(pinCoords);
        }

        function onMouseUp() {
            viewer.controls().enable();
            let compData = JSON.parse(localStorage.getItem(sceneId));
            if (compData && compData[hotspot._domElement.id] !== undefined && compData[hotspot._domElement.id]['position'] !== undefined) {
                compData[hotspot._domElement.id]['position'] = hotspot.position()
                localStorage.setItem(sceneId, JSON.stringify(compData));
            } else {
                const eleId = hotspot._domElement.id;
                if (compData === null) {
                    compData = {}
                }
                compData[eleId] = {position: hotspot.position()};
                localStorage.setItem(sceneId, JSON.stringify(compData));
            }
            window.removeEventListener("mousemove", onMouseMove);
            window.removeEventListener("mouseup", onMouseUp);
        }

        element.onmousedown = onMouseDown;
    }

    addStaticElementDrag(element, hotspot, sceneId) {
        let lastX, lastY;

        function onMouseDown(event) {
            lastX = event.pageX;
            lastY = event.pageY;
            window.addEventListener("mousemove", onMouseMove);
            window.addEventListener("mouseup", onMouseUp);
        }

        function onMouseMove(event) {
            const x = event.pageX;
            const y = event.pageY;
            const pinCoords = {x: `${(x / window.screen.width) * 100}%`, y: `${(y / window.screen.height) * 100}%`};
            hotspot.setAttribute('style', `top: ${pinCoords.y};left: ${pinCoords.x};transform: translateX(${x}px) translateY(${y}px) translateZ(0px)`)
            hotspot.setAttribute('data-x', `${x}`);
            hotspot.setAttribute('data-y', `${y}`);
        }

        function onMouseUp() {
            let compData = JSON.parse(localStorage.getItem(sceneId));
            let elePosition = element.getAttribute('style').split(";");
            let position = {}
            elePosition.forEach(function (element) {
                let ele = element.split(":")
                position[ele[0]] = ele[1].replace("%", "").replace(" ", "");
            });
            position["x"] = element.getAttribute('data-x');
            position["y"] = element.getAttribute('data-y');
            if (compData !== null && compData[element.getAttribute('id')] !== undefined && compData[element.getAttribute('id')]['position'] !== undefined) {
                compData[element.getAttribute('id')]['position'] = position
                localStorage.setItem(sceneId, JSON.stringify(compData));
            } else {
                if (compData === null) {
                    compData = {}
                }
                const eleId = element.getAttribute('id');
                compData[eleId] = {position: position};
                localStorage.setItem(sceneId, JSON.stringify(compData));
            }
            window.removeEventListener("mousemove", onMouseMove);
            window.removeEventListener("mouseup", onMouseUp);
        }

        element.onmousedown = onMouseDown;
    }

    /* ELEMENT DRAG END */

    async submitHotspots(e) {
        await dataScenes.saveScene(this.getRequestedScene(this.props), this.allLocalStorageRecord());
        e.preventDefault();
    }

    render() {
        const styleInfo = 'width: 100%; height:30px; background:#f6f6f6; border: 1px solid #000'
        const styleUrl = `${SERVICE_ADDR}scene/style/${this.state.sceneId}/${this.state.projectId}?token=${this.token}`
        return (
            <>
                <link href={styleUrl} rel="stylesheet"/>
                <div className="pano-container" ref={pano => this.pano = pano} id={this.state.sceneId}>
                    {/*<Header styleInfo={styleInfo}/>*/}
                    {this.state.show &&
                        <div className="SaveSceneInfo" onClick={this.submitHotspots}>
                            <SaveSceneButton/>
                        </div>
                    }
                    {this.state.navShow &&
                        <FloorNavigation/>
                    }
                </div>
            </>
        );
    }
}

export default withRouter(Pano);