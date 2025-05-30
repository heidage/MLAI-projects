'use client'

import * as React from 'react';
import { styled, useTheme, Theme, CSSObject } from '@mui/material/styles';
import List from '@mui/material/List';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import { Drawer, useMediaQuery } from '@mui/material';
import Person2Icon from '@mui/icons-material/Person2';
import EqualizerIcon from '@mui/icons-material/Equalizer';
import ExitToAppIcon from '@mui/icons-material/ExitToApp';
import { Settings } from '@mui/icons-material';

const drawerWidth = 240;

const openedMixin = (theme: Theme): CSSObject => ({
    width: drawerWidth,
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.enteringScreen,
    }),
    overflowX: 'hidden',
});

const closedMixin = (theme: Theme): CSSObject => ({
    transition: theme.transitions.create('width', {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    overflowX: 'hidden',
    width: `calc(${theme.spacing(7)} + 1px)`,
    [theme.breakpoints.up('sm')]: {
        width: `calc(${theme.spacing(8)} + 1px)`,
    },
});    

const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
}));

const menuRouteList = ['data', 'profile', 'settings', ""];
const menuListTranslations = ["Analytics", "Profile", "Settings","Sign Out"]
const menuListIcons = [
    <EqualizerIcon />,
    <Person2Icon />,
    <Settings/>,
    <ExitToAppIcon/>
]

const SideMenu = ()=>{
    const theme = useTheme();
    const [open, setOpen] = React.useState(false);
    const mobileCheck = useMediaQuery('(min-width:600px)');

    const handleDrawerToggle = () => {
        setOpen(!open);
    };

    return(
        <Drawer 
            variant="permanent"
            anchor='left'
            open={open}
            sx={{
                width: drawerWidth,
                [`& .MuiDrawer-paper`]: {
                    left: 0,
                    top: mobileCheck ? 64 : 57,
                    flexShrink: 0,
                    whiteSpace: 'nowrap',
                    boxSizing: 'border-box',
                    ...(open && {
                        ...openedMixin(theme),
                        '& .MuiDrawer-paper': openedMixin(theme),
                    }),
                    ...(!open && {
                        ...closedMixin(theme),
                        '& .MuiDrawer-paper': closedMixin(theme),
                    })
                },
            }}>
            <DrawerHeader>
                <IconButton onClick={handleDrawerToggle}>
                    {theme.direction === 'rtl' ? <ChevronRightIcon /> : <ChevronLeftIcon />}
                </IconButton>
            </DrawerHeader>
            <Divider />
            <Divider />
            <List>
            {menuListTranslations.map((text, index) => (
                <ListItem key={text} disablePadding sx={{ display: 'block' }}>
                <ListItemButton
                    sx={{
                    minHeight: 48,
                    justifyContent: open ? 'initial' : 'center',
                    px: 2.5,
                    }}
                >
                    <ListItemIcon
                    sx={{
                        minWidth: 0,
                        mr: open ? 3 : 'auto',
                        justifyContent: 'center',
                    }}
                    >
                    {menuListIcons[index]}
                    </ListItemIcon>
                    <ListItemText primary={text} sx={{ opacity: open ? 1 : 0 }} />
                </ListItemButton>
                </ListItem>
            ))}
            </List>
        </Drawer>
    )
}

export default SideMenu;
