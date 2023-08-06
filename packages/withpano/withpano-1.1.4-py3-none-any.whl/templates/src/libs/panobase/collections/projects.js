import {SERVICE_API_ADDR} from "../../constant";
import Swal from "sweetalert2";

class DataService {

    // --- GET ---

    async getProjects() {
        const token = JSON.parse(localStorage.getItem('token'));
        const fetchData = async () => {
            const requestOptions = {
                // method: 'GET',
                // mode: 'cors',
                headers: {
                    // 'Content-Type': 'application/json',
                    'x-access-token': 'Bearer ' + token.token
                },
            };
            const response = await fetch(SERVICE_API_ADDR + 'project/list/', requestOptions)
            if (!response.ok) {
                throw new Error('Data could not be fetched!')
            } else {
                return response.json()
            }
        }
        return fetchData()
    }

    async createProject(submitData) {
        const token = JSON.parse(localStorage.getItem('token'));
        console.log(submitData);
        const requestOptions = {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json',
                'x-access-token': 'Bearer ' + token.token
            },
            // headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({'name': submitData})
        };
        const project = fetch(SERVICE_API_ADDR + 'project/create/', requestOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error(response.statusText)
                }
                return response.json()
            })
            .catch(error => {
                Swal.showValidationMessage(
                    `Request failed: ${error}`
                )
            })
    }

}

export default new DataService();