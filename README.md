# pyproject-base

Python projects' base structure with files.

    git clone --depth 1 https://github.com/the-citto/pyproject-base <new-project-name>
(get only the last commit with `--depth 1`)

or, for bare repos (in folders)
    
    git clone --depth 1 file://<full>/<path>/<bare-repo-name>.git <new-project-name>

(if wanted, double check with `git remote` for `origin`)

detach the remote repo

    git remote remove origin

add the remote repo for the new project

    git remote add <path-to-new-remote-repo>

with `<path-to-new-remote-repo>` being the empty repo for the new python project

#
create package folder **in** `./python/` folder, `pyproject.toml` is set to read there instead of the standard `./src/`

     mkdir -p ./python/<project_name>/ && touch $_/__init__.py

**amend details in ** `README.md`, `LICENSE`, `pyproject.toml`, (if needed) `Makefile`

#

