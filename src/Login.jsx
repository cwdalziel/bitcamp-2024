import { useState } from 'react';
import CreateAccount from './CreateAccount'

const initLogin = {
    username: '',
    password: ''
}

function Login(props) {

    const [login, setLogin] = useState(initLogin)
    const [create, setCreate] = useState(false)

    const handleChange = (e) => {
        const { name, value } = e.target;
        setLogin({
            ...login,
            [name]: value
        })
    }

    const formSubmit = (res) => {
        props.setID(res.data.data.objectCreated._id)
    }

    return (<>
        {!create ? <> 
        <h1>Best App Ever?!?!</h1>
        <form>
            <input type='text' name='username' placeholder='Username' value={login.username} onChange={handleChange} />
            <input type='password' name='password' placeholder='Password' value={login.password} onChange={handleChange} />
            <input type="submit" value="Submit" />
        </form>
            <button onClick={() => setCreate(true)}>Create New Account</button> </> : <CreateAccount formSubmit={formSubmit} />}
    </>
    )

}

export default Login;