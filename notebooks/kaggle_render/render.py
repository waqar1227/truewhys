# TrueWhys Kaggle GPU render kernel. Renders background plates for one episode with Blender Cycles (OptiX/CUDA).
# Settings come from /kaggle/input/<dataset>/job.json: {"chapters": "0,1", "w":1920, "h":1080, "samples":128, "deadline": 39600}
import subprocess, glob, os, json, time, shutil
t0 = time.time()
cfgp = glob.glob('/kaggle/input/**/job.json', recursive=True)[0]
D = os.path.dirname(cfgp)
job = json.load(open(cfgp))
print("dataset dir", D, job, flush=True)
subprocess.run("nvidia-smi", shell=True)
if not os.path.exists('/tmp/blender/blender'):
    subprocess.run('wget -q https://download.blender.org/release/Blender5.0/blender-5.0.1-linux-x64.tar.xz -O /tmp/b.tar.xz && '
                   'mkdir -p /tmp/blender && tar -xf /tmp/b.tar.xz -C /tmp/blender --strip-components=1', shell=True, check=True)
subprocess.run('apt-get -qq install -y libxkbcommon0 libsm6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 >/dev/null 2>&1', shell=True)
B = '/tmp/blender/blender'
out = '/kaggle/working/plates'
os.makedirs(out, exist_ok=True)
ngpu = int(subprocess.run("nvidia-smi -L | wc -l", shell=True, capture_output=True, text=True).stdout.strip() or 1)
procs = []
for i in range(ngpu):
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(i))
    cmd = [B, '-b', '--python', f'{D}/render_bg.py', '--', f'{D}/shots.json', out, '--w', str(job['w']), '--h', str(job['h']),
           '--samples', str(job['samples']), '--gpu', '--part', f'{i}/{ngpu}', '--deadline', str(job.get('deadline', 39600))]
    if job.get('chapters'):
        cmd += ['--chapters', job['chapters']]
    if job.get('shots'):
        cmd += ['--shots_only', job['shots']]
    procs.append(subprocess.Popen(cmd, env=env, stdout=open(f'/kaggle/working/blender_{i}.log', 'w'), stderr=subprocess.STDOUT))
for p in procs:
    p.wait()
for f in glob.glob(f'{out}/_tmp_*'):
    shutil.rmtree(f, ignore_errors=True)
logs = "".join(open(f).read() for f in glob.glob(f'{out}/render_log_*.txt'))
open('/kaggle/working/summary.txt', 'w').write(f"gpus={ngpu} wall_min={(time.time()-t0)/60:.1f}\n" + logs)
print(open('/kaggle/working/summary.txt').read())
for i in range(ngpu):  # keep only the tail of blender logs
    L = open(f'/kaggle/working/blender_{i}.log').read().splitlines()
    open(f'/kaggle/working/blender_{i}.log', 'w').write("\n".join([l for l in L if 'Fra:' not in l][-200:]))
