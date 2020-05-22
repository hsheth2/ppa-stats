from fastapi import FastAPI
import app.stats as stats

app = FastAPI()

@app.get('/api/owner/{ppa_owner}/ppa/{ppa_name}/package/{package_name}/downloads')
def downloads(ppa_owner: str, ppa_name: str, package_name: str):
    binaries = stats.get_binaries(ppa_owner, ppa_name, package_name)

    downloads = []
    for binary in binaries:
        info = stats.get_binary_info(binary)
        
        downloads.append({
            'display_name': info['display_name'],
            'total_downloads': info['total_downloads'],
            'daily_downloads': dict(info['daily_downloads']),
        })

    return downloads


@app.get('/api/owner/{ppa_owner}/list_ppas')
def list_ppas(ppa_owner: str):
    lp = stats.launchpad
    owner = lp.people[ppa_owner]
    
    ppas = []
    for ppa in owner.ppas:
        ppas.append(ppa.name)
    return ppas
