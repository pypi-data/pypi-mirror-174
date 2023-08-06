import React, {useState} from "react";
import './App.css';
import {BrowserRouter, Redirect, Route, Switch, useHistory} from "react-router-dom";
import Landing from "./components/Landing";
import Login from "./components/Authentication/Login";
import useToken from "./libs/panobase/UseToken";
import Swal from "sweetalert2";
import LogoutButton from "./components/Authentication/LogoutButton";


export default function App() {
    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);
    const {token, setToken} = useToken();
    const history = useHistory();

    if (!token) {
        return <Login setToken={setToken}/>
    }
    const logout = function (event) {
        Swal.fire({
            title: 'Are you sure?',
            text: "You have to re-login for access any of the section!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Yes, Logout!!!'
        }).then((result) => {
            if (result.isConfirmed) {
                localStorage.removeItem('token');
                setToken(!token);
            }
        })
        event.preventDefault();
    }
    const inactivityTime = function () {
        let time;
        window.onload = resetTimer;
        // DOM Events
        document.onmousemove = resetTimer;
        document.onkeypress = resetTimer;

        function resetTimer() {
            clearTimeout(time);
            time = setTimeout(alert("Inactive Secction"), 3000)
        }
    };
    // inactivityTime();
    return (
        <BrowserRouter>
            <div onClick={logout}><LogoutButton/></div>
            <Switch>
                <Route path="/">
                    <div className="App">
                        <Landing/>
                    </div>
                </Route>
                <Redirect to='/'/>
            </Switch>
        </BrowserRouter>
    );
}