# Style R (close-to-human 3D) sample cast — how it was made (audit session, 15 Nov 2026)
Sheet: `docs/audit/review/style_r_cast_sheet.jpg`. CPU preview (48 samples); finals belong on Kaggle GPU.
All assets CC0: MPFB 2.0.18 (MakeHuman for Blender, GPL code, CC0 output/assets) + MakeHuman system assets pack (CC0).
1. MPFB: download from extensions.blender.org (`add-on-mpfb-v2.0.18.zip`, sha256 c075b3e9…2dad) and install into bpy:
   `bpy.ops.extensions.package_install_files(filepath=<zip>, repo="user_default", enable_on_install=True)`.
2. Assets: `files.makehumancommunity.org` is blocked from the cloud; `files2.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip`
   works but is very slow (~40 KB/s, 280 MB). `zipls.py <url> 280737770 get '<regex>' <outdir>` pulls only the needed files by HTTP range requests
   (geometry .obj/.mhclo/.mhmat + the hair/eyebrow/eyelash alpha .png). Clothes textures are not needed (flat brand colours are applied).
3. Render: replace ASSETS_DIR in `specs/*.json`, then `/opt/c3d/bin/python -I build.py specs/c_wy_full.json out.png 48`.
   Spec = macro body sliders, shape targets (head/eye scale for the stylised look, expression units for faces), skin colour, hair/clothes/shoes + colours,
   arm pose, props (Wy's badge), camera mode full|head. Two-colour outfits are split by mesh island (shirt vs trousers).
Missing for a full Style R episode: era costumes (Sketchfab CC0/CC-BY or modelled), teeth, hand poses/animation (Quaternius UAL, CC0).
