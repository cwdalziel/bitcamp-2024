import { useEffect, useState } from 'react';
import axios from 'axios';
import bg from './bg_1.gif'
import coinman from './New_Piskel_1.gif'
import opp1 from './New_Piskel.gif'
import opp2 from './Slots.gif'
import opp3 from './Boss.gif'
import './App.css';

const initTransaction = {
    amount: 0,
    date: '',
    desc: ''
}

function Budgeter(props) {

    const [transactions, setTransactions] = useState([])
    const [transaction, setTransaction] = useState(initTransaction)
    const [balance, setBalance] = useState(0)
    const [userHP, setUserHP] = useState(100)
    const [enemyHP, setEnemyHP] = useState(100)
    const [enemyID, setEnemyID] = useState(0)
    const [dead, setDead] = useState(false)

    useEffect(() => {
        update(0)
    }, [])

    if (dead) {
        props.lose()
    }

    const update = (damage) => {
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
        axios.post('http://localhost:8000/user/damage/' + props.user + '?damage=' + damage).then((res) => {
            setUserHP(res.data.user_hp)
            setEnemyHP(res.data.enemy_hp)
            setEnemyID(res.data.enemy_id)
            setDead(res.data.player_killed)
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
                update(transaction.amount)
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
            <div style={{display: 'flex',alignItems: 'center',justifyContent: 'center',}}>
                <span className="health">Player Health: {userHP}</span>
                <img className="bg" src={bg} height={800} width={800} alt='background' />
                <span className="health">Enemy Health: {enemyHP}</span>
            </div>
            <img className="coinman" src={coinman} height={512} width={512} alt='coinman' />
            <img className="opposition" src={enemyID === 0 ? opp1 : enemyID === 1 ? opp2 : opp3} height={400} width={400} alt='enemy' />
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
                <div>{entry.amount >= 0 ? <span className='positive'>${entry.amount}</span> : <span className='negative'>-${-entry.amount}</span>}, {entry.desc}, {entry.date} </div>
            </div>
        ))}
    </div>
    )
}

export default Budgeter