import os
import asyncio
from asyncio import TaskGroup
from Auth.MsalWindowsAuthenticator import MsalWindowsAuthenticator
from dotenv import load_dotenv
from Client.OriginClient import OriginClient
from DesignBehaviours.SpaceOutletsBehaviour import SpaceOutletsBehaviour
from DesignBehaviours.SpaceVentilationBehaviour import SpaceVentilationBehaviour

load_dotenv()

CLIENT_ID = os.environ.get('CLIENT_ID')
TENANT_ID = os.environ.get('TENANT_ID')
SCOPES = [os.environ.get('SCOPE_USER')]

async def main():
    winauth = MsalWindowsAuthenticator(CLIENT_ID, TENANT_ID, SCOPES)

    try:
        wtoken = winauth.GetAuthtoken()
        print("Token acquired successfully")
    except Exception as e:
        print(str(e))


    oclient = OriginClient("http://localhost:4002/graphql", "ws://localhost:4002/graphql", winauth)

    spaceTypeBehaviour1 = SpaceOutletsBehaviour(oclient)
    subresult1 = spaceTypeBehaviour1.Start()

    oclient2 = OriginClient("http://localhost:4002/graphql", "ws://localhost:4002/graphql", winauth)

    spaceTypeBehaviour2 = SpaceVentilationBehaviour(oclient2)
    subresult2 = spaceTypeBehaviour2.Start()

    try:
        async with TaskGroup() as group:
                    # spawn some tasks
                    group.create_task(subresult1)
                    group.create_task(subresult2)

                    # wait for 24 hours
                    await asyncio.sleep(60 * 60 * 24) 
                    raise Exception("Tasks timed out")
    except Exception as e:
            pass

    await oclient.Close()
    await oclient2.Close()


asyncio.run(main())