"use client";

import React from "react";
import { useSession, signIn, signOut } from "next-auth/react";
import { Avatar } from "@mui/material";
import Button from "@mui/material/Button";

const Login = ()=>{
    const {data: session } = useSession();
    const avatar = session?.user?.image as string;

    if (session){
        return <>
            <Button variant={'contained'} color={'error'} onClick={()=>signOut()}>Sign Out</Button>
        </>
    }
    return <>
        <h2>Please log in</h2> <br/>
        <Button variant={'contained'} color={'success'} onClick={()=>signIn()}>Sign In</Button>
    </>
}

export default Login;
