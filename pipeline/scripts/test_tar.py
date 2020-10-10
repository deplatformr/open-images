import tarfile
import os

external_identifier = "deplatformer-open-images-1"
batch_dir = "source_data/batches/1"

try:
    # Create the tar package
    packages_dir = os.path.join(
        os.getcwd(), "source_data/packages/")
    tarball_name = external_identifier + ".tar"
    tarball = tarfile.open(os.path.join(
        packages_dir, tarball_name), "w")
    tarball.add(batch_dir)
    tarball.close()
    print("created a tarball")  # debug
except Exception as e:
    print("Unable to create a tarball package from batch.")
    print(e)
