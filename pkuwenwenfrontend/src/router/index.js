import { createWebHistory, createRouter } from "vue-router"

const routes = [
    {
      path: '/',
      name: 'Home',
      component: () => import('../components/Home.vue')
    },
    {
        path: '/SignUpAsPatient',
        name: 'SignUpAsPatient',
        component: () => import('../components/Pages/SignUpAsPatient.vue')
    },
    {
        path: '/SignUpAsDoctor',
        name: 'SignUpAsDoctor',
        component: () => import('../components/Pages/SignUpAsDoctor.vue')
    },
    {
        path: '/PatientSignIn',
        name: 'PatientSignIn',
        component: () => import('../components/Pages/PatientSignIn.vue')
    },

    {
        path: '/DoctorSignIn',
        name: 'DoctorSignIn',
        component: () => import('../components/Pages/DoctorSignIn.vue')
    },
    {
        path: '/PatientHomepage',
        name: 'PatientHomepage',
        component: () => import('../components/Pages/PatientHomepage.vue')
    },
    {
        path: '/:office/DoctorIndex', //使用动态链接，office是院系名
        name: 'DoctorIndex',
        component: () => import('../components/Pages/DoctorIndex.vue')
    },
    {
        path: '/:school/:course/QuestionIndex',
        //path: '/Questions',
        name: 'QuestionIndex',
        component: () => import('../components/Pages/QuestionIndex.vue')
    },
    {
        path: '/Question/:id',
        name: 'Question',
        component: () => import('../components/Pages/Question.vue')
    },
    {
        path: '/Dashboard',
        name: 'Dashboard',
        component: () => import('../components/dashboard')
    },
    {
        path: '/ViewAnswer',
        name: 'ViewAnswer',
        component: () => import ('../components/Pages/ViewAnswer')
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

/*
router.beforeEach((to, from, next) => {
    document.title = `| PkuWenWen |`;
    const role = localStorage.getItem('ms_username');
    if (!role && to.path !== '/SignIn') {
        next('/SignIn');
    } else {
        next();
    }
})
*/

export default router
