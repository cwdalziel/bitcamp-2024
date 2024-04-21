import { useEffect, useState } from 'react';
import axios from 'axios';

const initTransaction = {
    amount: 0,
    date: '',
    desc: ''
}

function Budgeter(props) {

    const [transactions, setTransactions] = useState([])
    const [transaction, setTransaction] = useState(initTransaction)
    const [balance, setBalance] = useState(0)

    useEffect(() => {
        update()
    }, [])

    const update = () => {
        axios.get('http://localhost:8000/user/stats/' + props.user).then((res) => {
            setTransactions(res.data.data.sort((a, b) => {
                return new Date(b.date) - new Date(a.date);
            }))
        }).catch((err) => {
            console.log(err)
        })
        axios.get('http://localhost:8000/user/balance/' + props.user).then((res) => {
            setBalance(res.data.data)
        }).catch((err) => {
            console.log(err)
        })
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        if (transaction.date !== '') {
            axios.post('http://localhost:8000/user/stats/add', {
                amount: transaction.amount,
                date: transaction.date,
                desc: transaction.desc
            }, {
                params: { username: props.user }
            }).then(() => {
                update()
                setTransaction(initTransaction)
            }).catch((err) => {
                console.log(err)
            })
        }
    }

    const handleChange = (e) => {
        const { name, value } = e.target;
        setTransaction({
            ...transaction,
            [name]: value
        })
    }

    return (<div>
        <div>
            Balance: {balance}
        </div>
        <form onSubmit={handleSubmit}>
            <input type='number' name='amount' placeholder='Amount' value={transaction.amount} onChange={handleChange} />
            <input type='date' name='date' value={transaction.date} onChange={handleChange} />
            <input type='text' name='desc' placeholder='Desciption' value={transaction.desc} onChange={handleChange} />
            <input className="button" type="submit" value="Submit" />
        </form>
        {transactions.map((entry, index) => (
            <div className="transaction" key={index}>
                <div>{entry.amount} {entry.desc} {entry.date} </div>
            </div>
        ))}
    </div>
    )
}

export default Budgeter