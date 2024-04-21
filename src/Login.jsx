import { useState } from 'react';
import CreateAccount from './CreateAccount'
import axios from 'axios'
import './App.css';

const initLogin = {
    username: '',
    password: ''
}

function Login(props) {

    const [login, setLogin] = useState(initLogin)
    const [create, setCreate] = useState(false)
    const [errMsg, setErrMsg] = useState('')

    const handleChange = (e) => {
        const { name, value } = e.target;
        setLogin({
            ...login,
            [name]: value
        })
    }

    const formSubmit = (res) => {
        props.setID(res.data.id)
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://localhost:8000/get_player_id', {
            username: login.username,
            password: login.password,
        }).then((res) => {
            props.setID(res.data.id)
        }).catch((err) => {
            console.log(err)
            setErrMsg(err.response.data.detail)
        })
    }

    return (<>
        {!create ? <>
            <h1>Best App Ever?!?!</h1>
            <form onSubmit={handleSubmit}>
                <input className="input" type='text' name='username' placeholder='Username' value={login.username} onChange={handleChange} />
                <input className="input" type='password' name='password' placeholder='Password' value={login.password} onChange={handleChange} />
                <input className="button" type="submit" value="Submit" />
            </form>
            <button className="button" onClick={() => setCreate(true)}>Create New Account</button>
            <div className="error-msg">{errMsg}</div>
        </>
            : <CreateAccount formSubmit={formSubmit} />}
    </>
    )

}

export default Login;