import {SERVICE_API_ADDR} from "../../constant";

class DataService {

    // --- GET ---

    async getScene(scene, project) {
        const token = JSON.parse(localStorage.getItem('token'));
        const requestOptions = {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'x-access-token': 'Bearer ' + token.token
            }
        };
        const fetchData = async () => {
            const response = await fetch(SERVICE_API_ADDR + 'scenes/scene/' + scene + '/' + project, requestOptions)
            if (!response.ok) {
                throw new Error('Data could not be fetched!')
            } else {
                return response.json()
            }
        }
        return fetchData()
    }

    async saveScene(scene, submitData) {
        console.log(submitData);
        const token = JSON.parse(localStorage.getItem('token'));
        const requestOptions = {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'x-access-token': 'Bearer ' + token.token
            },
            // headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(submitData)
        };
        fetch(SERVICE_API_ADDR + 'scenes/scene/save/' + scene.sceneId + '/' + scene.projectId, requestOptions)
            .then(response => console.info(response.json()));
    }

    cleanStorage() {
        let archive = [], // Notice change here
            keys = Object.keys(localStorage),
            i = keys.length;
        while (i--) {
            if (keys[i].includes("ids")) {
                const storageData = JSON.parse(localStorage.getItem(keys[i]))
                localStorage.removeItem(keys[i]);
            }
        }
        return "Success";
    }

    async getSceneImage(scene, project) {
        const token = JSON.parse(localStorage.getItem('token'));
        const requestOptions = {
            method: 'GET',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'x-access-token': 'Bearer ' + token.token
            }
        };
        const fetchData = async () => {
            const response = await fetch(SERVICE_API_ADDR + 'scenes/scene/image/' + scene + '/' + project, requestOptions)
            if (!response.ok) {
                throw new Error('Data could not be fetched!')
            } else {
                console.log(response.json())
                return response
            }
        }
        return fetchData()
    }

}

export default new DataService();