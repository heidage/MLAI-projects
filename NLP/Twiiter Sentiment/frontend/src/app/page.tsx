import Image from 'next/image'
import styles from './page.module.css'
import Dashboard from './dashboard/page'
import Header from '@/components/Header'
import SideMenu from '@/components/SideMenu'

export default function Home() {
  return (
    <main className={styles.main}>
      <Header/>
      <SideMenu/>
      <Dashboard/>
    </main>
  )
}
