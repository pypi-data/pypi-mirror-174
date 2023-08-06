import {SERVICE_API_ADDR} from "../../constant";
import Swal from "sweetalert2";

class DataService {

    async loginUser(credentials) {
        return fetch(SERVICE_API_ADDR + 'auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(credentials)
        }).then(data => data.json());
    }
}

export default new DataService();