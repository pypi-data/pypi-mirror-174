import {circle, info, link, outside, question, video,} from '../images/images';
import {SERVICE_ADDR} from "./constant";

class TourSettings {

    getDefaultScene() {
        return "Outside";
    }

    getTourScene() {
        return "MetaVerseRoom";
    }

    getNewUser() {
        const newUser = {name: null, canPickupKey: true};
        return newUser;
    }

    getSceneImage(sceneName, projName) {
        if (sceneName === 'default') {
            return outside
        } else {
            const token = JSON.parse(localStorage.getItem('token'));
            return SERVICE_ADDR + "scene/image/" + sceneName + "/" + projName + "?token=" + token.token
        }
    }

    getHotspotImage(hotspotType) {
        switch (hotspotType) {
            default:
                return circle;
            case 'link':
                return link;
            case 'info':
                return info;
            case 'infoAnimation':
                return info;
            case 'question':
                return question;
            case 'video':
                return video;
        }
    }

    getHotspotInfo(hotspotType) {
        switch (hotspotType) {
            default:
                return false;
            case 'info':
            case 'video':
                return true;
        }
    }

}

export default new TourSettings();