corruption_types=('pop_ups' 'resolution' 'marks' 'subtitle' 'multi_apps' 'accidential_touch' 'app_minimization' 'network_error' 'verification')

for corruption_type in "${corruption_types[@]}"; do
    python run.py --noise_type $corruption_type
done