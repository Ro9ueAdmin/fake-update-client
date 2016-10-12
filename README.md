## Mender dummy update client

This script/Dockerfile allows you to spawn many fake mender clients, of different device type. These client will simulate an update, and either pass or fail, depending on arguments supplied to them.

This tool wraps around `mender-backend-cli` tool and uses Docker containers in order to run concurrently

##### Example using Docker:

- Build the Docker container: 

    `docker build -t fake-client .`
- Run the Docker container, with specificed arguments:
    
    - Run a client that can successfully update and identifies as a beaglebone:
    
        `docker run -d -e DEVICE='beaglebone' --network=integration_mender -t fake-client`

    - Run a client that fails, and sends custom inventory data:
    
        `docker run -d -e INVENTORY='device_type:beaglebone,image_id:fake-device' -e FAIL='error msg' --network=integration_mender -t fake-client`

- And of course, to make multiple fake clients (without docker compose):
- 
    - Using zsh: `repeat 10 { docker run -d -e INVENTORY='device_type:beaglebone' --network=integration_mender -t fake-client }`


    - Using bash: `for n in {1..5}; do docker run -d -e INVENTORY='device_type:beaglebone' --network=integration_mender -t fake-client; done`

