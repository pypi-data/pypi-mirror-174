import {SERVICE_API_ADDR} from "../../constant";


class DataService {
    // --- GET ---
    async getSceneHotspots(scene) {
        const fetchData = async () => {
            const response = await fetch(SERVICE_API_ADDR + 'scenes/hotspot/' + scene)
            if (!response.ok) {
                throw new Error('Data could not be fetched!')
            } else {
                return response.json()
            }
        }
        return fetchData()
    }

    async createSceneHotspot(scene, hotspot) {
        console.info(JSON.stringify(hotspot));
        const token = JSON.parse(localStorage.getItem('token'));
        const requestOptions = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-access-token': 'Bearer ' + token.token
            },
            body: JSON.stringify(hotspot)
        };
        fetch(SERVICE_API_ADDR + 'scenes/scene/hotspot/' + scene, requestOptions)
            .then(response => console.info(response.json()))
            .then(data => console.info("RESPONSE", data));
    }
}

export default new DataService();