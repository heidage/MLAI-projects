"use client";

import React from "react";
import { useSession, signIn, signOut } from "next-auth/react";
import { Avatar } from "@mui/material";

const Login = ()=>{
    const {data: session } = useSession();

    if (session){
        return <>
            Signed in as {session?.user?.email} <br/>
            <p>Welcome {session?.user?.name}</p>
            <Avatar alt={session?.user?.name} src={session?.user?.image}/>
            <button onClick={()=>signOut()}>Sign Out</button>
        </>
    }
    return <>
        Not signed in <br/>
        <button onClick={()=>signIn()}>Sign In</button>
    </>
}

export default Login;
