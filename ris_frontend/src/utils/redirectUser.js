import { useRouter } from 'next/navigation';

export function useRedirectUser() {
    const router = useRouter();

    const redirectUser = () => {
        const accessToken = localStorage.getItem('access_token');

        if (!accessToken) {
            // Redirect to login page if access_token is not present
            router.push('/login');
            return;
        }

        // If access_token is present, redirect to home and handle role_id
        const roleId = localStorage.getItem('role_id');

        switch (roleId) {
            case '1':
                router.push('/home/waiter');
                break;
            case '2':
                router.push('/home/chef');
                break;
            case '3':
                router.push('/home/manager');
                break;
            default:
                // Handle case where role_id is not recognized
                console.warn('Unknown role_id:', roleId);
                router.push('/home'); // Default redirection
                break;
        }
    };

    return { redirectUser };
}
