from ast import Store
import os
import argparse


if __name__=="__main__":
    # add arg parse
    parser = argparse.ArgumentParser(description="升级脚本使用说明")
    parser.add_argument('--update-middle-version', help='increse middle version', action='store_true')
    parser.add_argument('--update-major-version', help='increse big version', action='store_true')
    args = parser.parse_args()


    # check if current git work tree is clean and has no untracked files
    # if yes, checkout to release branch else exit
    if not os.system("git diff --quiet && git diff --cached --quiet"):
        # if release and dev on the same commit, exit
        if os.system("git rev-parse --abbrev-ref HEAD") == "release":
            print("release branch is on the same commit as dev branch, exit")
            exit(1)

        # checkout to release branch
        os.system("git checkout release")
        # merge dev branch to release branch
        os.system("git merge dev")
        # if merge success, push release branch to remote
        if not os.system("git diff --quiet && git diff --cached --quiet"):
            # read the latest tag
            latest_tag = os.popen("git describe --abbrev=0 --tags").read()
            # get the latest tag version
            latest_tag_version = latest_tag.split("v")[1]
            # increase the latest tag version
            latest_tag_version = latest_tag_version.split(".")
            # if update major version
            if args.update_major_version:
                latest_tag_version[0] = str(int(latest_tag_version[0]) + 1)
                latest_tag_version[1] = "0"
                latest_tag_version[2] = "0"
            # if update middle version
            elif args.update_middle_version:
                latest_tag_version[1] = str(int(latest_tag_version[1]) + 1)
                latest_tag_version[2] = "0"
            # if update minor version
            else:
                latest_tag_version[2] = str(int(latest_tag_version[2]) + 1)
            # join the latest tag version
            latest_tag_version = ".".join(latest_tag_version)
            # create new tag
            os.system(f"git tag v{latest_tag_version}")
            # push tag to remote
            os.system(f"git push origin v{latest_tag_version}")
            # push release branch to remote
            os.system("git push origin release")
            # run tox -e publish
            os.system("python3 -m tox -e build && python3 -m tox -e publish -- --repository pypi")

            if not os.system("git diff --quiet && git diff --cached --quiet"):
                os.system("git checkout dev")

        else:
            # abort merge
            os.system("git merge --abort")

    else:
        # exit
        print("git work tree is not clean, please commit and push your changes first")
        exit(1)
