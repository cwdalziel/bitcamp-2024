import { useState } from 'react'
import axios from 'axios'

const initValues = {
    username: '',
    password: '',
    firstName: '',
    lastName: '',
    streetNum: '',
    streetName: '',
    city: '',
    state: '',
    zip: ''
}

function CreateAccount(props) {

    const [values, setValues] = useState(initValues)
    const [errMsg, setErrMsg] = useState('')

    const handleChange = (e) => {
        const { name, value } = e.target;
        setValues({
            ...values,
            [name]: value
        })
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.post('http://localhost:8000/new_player', {
            username: values.username,
            password: values.password,
            customer: {
                first_name: values.firstName,
                last_name: values.lastName,
                address: {
                    street_number: values.streetNum,
                    street_name: values.streetName,
                    city: values.city,
                    state: values.state,
                    zip: values.zip
                }
            }
        }).then((res) => {
            props.formSubmit(res)
        }).catch((err) => {
            console.log(err)
            setErrMsg(err.response.data.detail)
        })
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <div>
                    <input type='text' name='username' placeholder='Username' value={values.username} onChange={handleChange} />
                    <input type='password' name='password' placeholder='Password' value={values.password} onChange={handleChange} />
                </div>
                <div>
                    <input type='text' name='firstName' placeholder='First Name' value={values.firstName} onChange={handleChange} />
                    <input type='text' name='lastName' placeholder='Last Name' value={values.lastName} onChange={handleChange} />
                </div>
                <div>
                    <input type='text' name='streetNum' placeholder='Street Number' value={values.streetNum} onChange={handleChange} />
                    <input type='text' name='streetName' placeholder='Street Name' value={values.streetName} onChange={handleChange} />
                </div>
                <div>
                    <input type='text' name='city' placeholder='City' value={values.city} onChange={handleChange} />
                    <input type='text' name='state' placeholder='State' value={values.state} onChange={handleChange} />
                    <input type='text' name='zip' placeholder='Zip Code' value={values.zip} onChange={handleChange} />
                </div>
                <input type="submit" value="Submit" />
            </form>
            <label>{errMsg}</label>
        </div>
    )
}

export default CreateAccount