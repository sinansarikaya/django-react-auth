import React, { useEffect, useState } from 'react'
import { useNavigate } from "react-router-dom"
import useAuth from '../../hooks/useAuth'
import useLogout from "../../hooks/useLogout"
import useUser from '../../hooks/useUser'

export default function User() {

    const { user } = useAuth()

    const navigate = useNavigate()
    const logout = useLogout()
    const [loading, setLoading] = useState(false)
    const getUser = useUser()

    useEffect(() => {
        getUser()
    }, [])


    async function onLogout() {
        setLoading(true)

        await logout()
        navigate('/')
    }
    
    return (
        <div>
            <h3>{user?.username}</h3>
            <h4>{user?.email}</h4>
            <button disabled={loading} type='button' onClick={onLogout}>Logout</button>
        </div>
    )
}
