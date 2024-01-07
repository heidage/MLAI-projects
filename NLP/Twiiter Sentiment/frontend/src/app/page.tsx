import Dashboard from './dashboard/page'
import SideMenu from '@/components/SideMenu'
import Head from 'next/head'
import Login from '@/components/Login'
import scss from './page.module.scss'

export default function Home() {
  return (
    <>
      <Head>
        <title>Facebook Data Dashboard</title>
        <meta name="description" content="Twitter Data Dashboard" />
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={scss.main}>
        <SideMenu/>
        <Dashboard/>
        <Login/>
      </main>
    </>
  )
}
