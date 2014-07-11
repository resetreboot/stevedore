# -*- coding: utf-8 -*-
#!/usr/bin/env python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import docker

class DockerImage(object):
    """
    This class hold all the image information we could possibly need.
    """
    def __init__(self, 
                 repository,
                 tag,
                 img_id,
                 created,
                 size,
                 virtual_size):
        self.repository = repository
        self.tag = tag
        self.img_id = img_id
        self.created = created
        self.size = size
        self.virtual_size = virtual_size

    def __str__(self):
        return self.__unicode__()

    def __unicode__(self):
        return unicode(self.repository) + u":" + unicode(self.tag)

    def __repr__(self):
        return u"DockerImage: <" + unicode(self) + u">"


class DockerContainer(object):
    """
    Class for holding all the container information available
    """
    # Status constants 
    UP = 1
    EXITED = 0
    UNKNOWN = -1

    def __init__(self, container_id, image, command, created, names):
        self.container_id = container_id
        self.image = image
        self.command = command
        self.created = created
        self.names = self.filter_names(names)
        self.status = DockerContainer.UNKNOWN
        self.time_elapsed = 0
        self.ports = []

    def filter_names(self, list_names):
        """
        Removes the starting slash from the names and returns the list
        """
        return [ elem.replace(r'/', '') for elem in list_names]

    def update_status(self, status, time_elapsed):
        """
        Sets the current status of the container
        """
        self.status = status
        self.time_elapsed = time_elapsed

    def add_port(self, port = None, host_port = None, links = [], docker_port = None):
        """
        Adds a port description to the container
        """
        if docker_port is not None and docker_port not in self.ports:
            self.ports.append(docker_port)

        elif port is not None:
            port_description = DockerPort(port, host_port, links)

            if port_description not in self.ports:
                self.ports.append(port_description)

        else:
            raise TypeError("Must specify either a port description or a port object")

    def status_from_string(self, status_string):
        """
        Returns a tuple with the container's status from the status string
        """
        if 'Exited' in status_string:
            self.status = DockerContainer.EXITED
            self.time_elapsed = u" ".join(status_string.split()[2:])

        elif 'Up' in status_string:
            self.status = DockerContainer.UP
            self.time_elapsed = u" ".join(status_string.split()[1:])

        else:
            self.status = DockerContainer.UNKNOWN
            self.time_elapsed = ""

    def return_status_string(self):
        status_texts = { DockerContainer.UP : u'Up ',
                         DockerContainer.EXITED : u'Exited ',
                         DockerContainer.UNKNOWN : u'Unknown status ' }
        
        return status_texts[self.status] + self.time_elapsed

    def __str__(self):
        return unicode(self)

    def __unicode__(self):
        if len(self.names) > 1:
            names = unicode(self.names[0]) + u" (" + u", ".join(self.names[1:]) + u")"

        else:
            names = unicode(self.names[0])
            
        return names + u" id: " + unicode(self.container_id) + u" " + self.return_status_string()

    def __repr__(self):
        return u"DockerContainer: <" + unicode(self.names[0]) + " ID:" + unicode(self.container_id) + u">"


class DockerPort(object):
    """
    Encapsulates Docker container's ports
    """
    def __init__(self, port, host_port = None, links = []):
        self.port = port
        self.host_port = host_port
        self.links = links

    def add_link(self, container_name):
        if container_name not in self.links:
            self.links.append(container_name)

    def remove_link(self, container_name):
        try:
            self.links.remove(container_name)

        except ValueError as e:
            pass


class DockerInterface(object):
    """
    This class encapsulates the docker command line into nice methods for us to work with it.
    """
    def __init__(self, 
                 docker_url = 'unix://var/run/docker.sock', 
                 connect_timeout = 10):
        # Connect to the docker server, if this fails we let it go up
        try:
            self.client = docker.Client(base_url = docker_url, 
                                        timeout = connect_timeout)

        except Exception as e:
            self.client = None
            raise e

        # Since we're connected, let's get all the containers and images available
        self.update_images()
        self.update_containers()

    def update_images(self):
        """
        Ask our docker server which images we've got available to run and store
        it in ourselves for future reference.
        """
        self.images = []
        if self.client is not None:
            img_list = self.client.images()
            for img_info in img_list:
                for repo_tags in img_info['RepoTags']:
                    repository_and_tags = repo_tags.split(':')
                    docker_image = DockerImage(repository = repository_and_tags[0],
                                               tag = repository_and_tags[1],
                                               img_id = img_info['Id'],
                                               created = img_info['Created'],
                                               size = img_info['Size'],
                                               virtual_size = img_info['VirtualSize'])

                    self.images.append(docker_image)

        else:
            raise DockerNotConnectedException()

    def update_containers(self):
        """
        Ask our docker server the containers created and their status
        """
        self.containers = dict()
        if self.client is not None:
            containers = self.client.containers(all = True)
            for container in containers:
                container_object = DockerContainer(container_id = container['Id'],
                                                   image = container['Image'],
                                                   command = container['Command'],
                                                   created = container['Created'],
                                                   names = container['Names'])

                container_object.status_from_string(container['Status'])
                self.containers[container['Id']] = container_object

        else:
            raise DockerNotConnectedException()


    def get_container_by_id(self, container_id):
        """
        Returns the container that matched container_id
        """
        if self.client is None:
            raise DockerNotConnectedException()

        return self.containers.get(container_id, None)

    def build(self, path, tag):
        """
        Creates a new docker image from a Dockerfile in the specified path
        """
        if self.client is not None:
            self.client.build(path = path, tag = tag)
            self.update_images()
            self.update_containers()

        else:
            raise DockerNotConnectedException()

    def remove_container(self, container_id):
        '''
        Removes a container based on it's ID.
        
        @param container_id: ID of the container to remove
        @type container_id: String
        '''
        if self.client is not None:
            self.client.remove_container(container_id)

        else:
            raise DockerNotConnectedException()


class DockerNotConnectedException(Exception):
    pass
