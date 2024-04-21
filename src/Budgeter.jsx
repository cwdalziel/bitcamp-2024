import { useEffect, useState } from 'react';
import axios from 'axios';
import bg from './bg_1.gif'
import coinman from './New_Piskel_1.gif'
import opposition from './New_Piskel.gif'

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
    })

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
            <img className="bg" src={bg} height={800} width={800} alt='background' />
            <img className="coinman" src={coinman} height={512} width={512} alt='coinman' />
            <img className="opposition" src={opposition} height={400} width={400} alt='enemy' />
        </div>
        <div className="balance">
            <span>Balance: </span>{balance >= 0 ? <span className='positive'>${balance}</span> : <span className='negative'>-${-balance}</span>}
        </div>
        <form className="form" onSubmit={handleSubmit}>
            <input type='number' name='amount' placeholder='Amount' value={transaction.amount} onChange={handleChange} />
            <input type='date' name='date' value={transaction.date} onChange={handleChange} />
            <input type='text' name='desc' placeholder='Desciption' value={transaction.desc} onChange={handleChange} />
            <input className="button" type="submit" value="Submit" />
        </form>
        {transactions.map((entry, index) => (
            <div className="transaction" key={index}>
                <div>${entry.amount}, {entry.desc}, {entry.date} </div>
            </div>
        ))}
    </div>
    )
}

export default Budgeter