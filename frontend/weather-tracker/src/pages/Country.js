import { useParams } from 'react-router-dom'
// import Button from 'react-bootstrap/Button'
// import 'bootstrap/dist/css/bootstrap.min.css'
import Navbar from '../components/Navbar'

export default function Country() {
    const params = useParams()
    return (
        <div>
            <Navbar />
            <h1>Country is {params.name}</h1>
        </div>
    )
}