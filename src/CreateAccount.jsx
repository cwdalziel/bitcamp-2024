import { useState } from 'react'

const initValues = {
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

    const handleChange = (e) => {
        const {name, value} = e.target;
        setValues({
            ...values,
            [name]: value
        })
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        props.formSubmit(values)
    }

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <input type='text' name='firstName' placeholder='First Name' value={values.firstName} onChange={handleChange}/>
                <input type='text' name='lastName' placeholder='Last Name' value={values.lastName} onChange={handleChange}/>
            </div>
            <div>
                <input type='text' name='streetNum' placeholder='Street Number' value={values.streetNum} onChange={handleChange}/>
                <input type='text' name='streetName' placeholder='Street Name' value={values.streetName} onChange={handleChange}/>
            </div>
            <div>
                <input type='text' name='city' placeholder='City' value={values.city} onChange={handleChange}/>
                <input type='text' name='state' placeholder='State' value={values.state} onChange={handleChange}/>
                <input type='text' name='zip' placeholder='Zip Code' value={values.zip} onChange={handleChange}/>
            </div>
            <input type="submit" value="Submit" />
        </form>
    )
}

export default CreateAccount