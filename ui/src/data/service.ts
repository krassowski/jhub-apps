import { JupyterHubService } from '../types/service';
export const services: JupyterHubService[] = [
  {
    name: 'JupyterLab',
    url: 'http://127.0.0.1:8000/user/jbouder/lab',
    external: true,
  },
  {
    name: 'Argo Workflows',
    url: '/hub/argo',
    external: false,
  },
  {
    name: 'User Management',
    url: '/auth/admin/nebari/console/',
    external: false,
  },
  {
    name: 'Environments',
    url: '/hub/conda-store',
    external: false,
  },
  {
    name: 'Monitoring',
    url: '/hub/monitoring',
    external: false,
  },
];
