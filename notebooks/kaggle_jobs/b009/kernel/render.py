# TrueWhys Kaggle GPU kernel for B-009 Style T plates (Blender 5.0.1 Cycles). Dataset (flat): sets.py, sets9.py, plates.py, job.json.
import subprocess, glob, os, json, time, shutil
t0 = time.time()
cfgp = glob.glob('/kaggle/input/**/job.json', recursive=True)[0]
D = os.path.dirname(cfgp); job = json.load(open(cfgp))
print("dataset dir", D, job, flush=True)
subprocess.run("nvidia-smi", shell=True)
if not os.path.exists('/tmp/blender/blender'):
    subprocess.run('wget -q https://download.blender.org/release/Blender5.0/blender-5.0.1-linux-x64.tar.xz -O /tmp/b.tar.xz && '
                   'mkdir -p /tmp/blender && tar -xf /tmp/b.tar.xz -C /tmp/blender --strip-components=1', shell=True, check=True)
subprocess.run('apt-get -qq install -y libxkbcommon0 libsm6 libxi6 libxxf86vm1 libxfixes3 libxrender1 libgl1 >/dev/null 2>&1', shell=True)
B = '/tmp/blender/blender'
W = '/tmp/work'; shutil.copytree(D, W, dirs_exist_ok=True)
out = '/kaggle/working/plates'; os.makedirs(out, exist_ok=True)
keys = []
for line in open(f"{W}/plates.py"):
    line = line.strip()
    if line.startswith('"') and '": ("' in line:
        keys.append(line.split('"')[1])
if job.get("only"):
    keys = [k for k in keys if k in job["only"].split(",")]
ngpu = int(subprocess.run("nvidia-smi -L | wc -l", shell=True, capture_output=True, text=True).stdout.strip() or 1)
procs = []
for i in range(ngpu):
    part = ",".join(keys[i::ngpu])
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(i))
    cmd = [B, '-b', '--python', f'{W}/plates.py', '--', out, str(job['w']), str(job['h']), str(job['samples']), '--gpu', '--only', part]
    procs.append(subprocess.Popen(cmd, env=env, cwd=W, stdout=open(f'/kaggle/working/blender_{i}.log', 'w'), stderr=subprocess.STDOUT))
for p in procs:
    p.wait()
logs = "".join(l for i in range(ngpu) for l in open(f'/kaggle/working/blender_{i}.log') if l.startswith('PLATE') or 'Error' in l)
open('/kaggle/working/summary.txt', 'w').write(f"gpus={ngpu} wall_min={(time.time()-t0)/60:.1f} plates={len(os.listdir(out))}/{len(keys)}\n" + logs)
print(open('/kaggle/working/summary.txt').read())
for i in range(ngpu):
    L = open(f'/kaggle/working/blender_{i}.log').read().splitlines()
    open(f'/kaggle/working/blender_{i}.log', 'w').write("\n".join([l for l in L if 'Fra:' not in l and 'Sample' not in l][-200:]))
