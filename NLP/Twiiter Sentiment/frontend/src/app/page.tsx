import styles from './page.module.css'
import Dashboard from './dashboard/page'
import Header from '@/components/Header'
import SideMenu from '@/components/SideMenu'
import Head from 'next/head'
import Login from '@/components/Login'

export default function Home() {
  return (
    <>
      <Head>
        <title>Twitter Data Dashboard</title>
        <meta name="description" content="Twitter Data Dashboard" />
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={styles.main}>
        <Header/>
        <SideMenu/>
        <Dashboard/>
        <Login/>
      </main>
    </>
  )
}
