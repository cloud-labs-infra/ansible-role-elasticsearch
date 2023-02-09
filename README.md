# ansible-role-elasticsearch

Ansible role for 7+ Elasticsearch

## Usage

Create your playbook yaml adding the role elasticsearch.
The application of the elasticsearch role results in the installation of a node on a host.

The simplest configuration therefore consists of:

```yaml
- name: Simple Example
  hosts: localhost
  roles:
    - role: geerlingguy.java
    - role: cloud_labs.elasticsearch_cluster
```

The above installs Elasticsearch in a single node 'node1' on the hosts 'localhost'.


### Basic Elasticsearch Configuration

All Elasticsearch configuration parameters are supported.  This is achieved using a configuration map parameter 'es_config' which is serialized into the elasticsearch.yml file.

In addition to the es_config map, several other parameters are supported for additional functions e.g. script installation.  These can be found in the role's defaults/main.yml file.

The following illustrates applying configuration parameters to an Elasticsearch instance.

```yaml
- name: Elasticsearch with custom configuration
  hosts: localhost
  roles:
    - role: geerlingguy.java
    - role: elastic.elasticsearch_cluster
  vars:
    es_data_dirs:
      - "/opt/elasticsearch/data"
    es_log_dir: "/opt/elasticsearch/logs"
    es_config:
      node.name: "node1"
      cluster.name: "custom-cluster"
      discovery.seed_hosts: "localhost:9301"
      http.port: 9201
      transport.port: 9301
      node.data: false
      node.master: true
    es_http_port: 9201
```


### Multi Node Server Installations

Multi node server installations with TLS settings and built-in users settings.

group_vars/all.yml

```yaml
elasticsearch_tmp_path: "/tmp/elasticsearch"
elasticsearch_docker_image: "elasticsearch:7.17.7"
test_certs_local_path: "{{ playbook_dir }}/test_certs/"
```

main.yml


```yaml
- name: Converge
  hosts: elasticsearch_master
  become: yes
  roles:
    - role: geerlingguy.java
    - role: cloud_labs.elasticsearch_cluster
      vars:
        es_elastic_password: elastic_password
        es_kibana_system_password: kibana_system_password
        es_logstash_system_password: logstash_system_password
        es_beats_system_password: beats_system_password
        es_apm_system_password: apm_system_password
        es_remote_monitoring_user_password: remote_monitoring_user_password
        es_network_host: 0.0.0.0
        es_enable_http_ssl: true
        es_enable_transport_ssl: true
        es_ssl_certificate_authority: "molecule/three_nodes_tls/test_certs/ca/ca.crt"
        es_ssl_key: "molecule/three_nodes_tls/test_certs/elasticsearch_master/elasticsearch_master.key"
        es_ssl_certificate: "molecule/three_nodes_tls/test_certs/elasticsearch_master/elasticsearch_master.crt"
        es_validate_certs: false
        es_config:
          cluster.name: "test-cluster"
          cluster.initial_master_nodes:
            - elasticsearch_master
          discovery.seed_hosts:
            - 172.18.0.3
            - 172.18.0.4
          http.host: "{{ es_network_host }}"
          http.port: 9200
          node.data: true
          node.master: true
          transport.host: "{{ es_network_host }}"
          transport.port: 9300
          bootstrap.memory_lock: false

- name: Converge node 1
  hosts: elasticsearch_node_1
  become: yes
  roles:
    - role: geerlingguy.java
    - role: cloud_labs.elasticsearch_cluster
      vars:
        es_network_host: 0.0.0.0
        es_enable_http_ssl: true
        es_enable_transport_ssl: true
        es_ssl_certificate_authority: "molecule/three_nodes_tls/test_certs/ca/ca.crt"
        es_ssl_key: "molecule/three_nodes_tls/test_certs/elasticsearch_node_1/elasticsearch_node_1.key"
        es_ssl_certificate: "molecule/three_nodes_tls/test_certs/elasticsearch_node_1/elasticsearch_node_1.crt"
        es_validate_certs: false
        es_config:
          cluster.name: "test-cluster"
          discovery.seed_hosts:
            - 172.18.0.2
            - 172.18.0.4
          http.host: "{{ es_network_host }}"
          http.port: 9200
          node.data: true
          node.master: false
          transport.host: "{{ es_network_host }}"
          transport.port: 9300
          bootstrap.memory_lock: false

- name: Converge node 2
  hosts: elasticsearch_node_2
  become: yes
  roles:
    - role: geerlingguy.java
    - role: cloud_labs.elasticsearch_cluster
      vars:
        es_network_host: 0.0.0.0
        es_enable_http_ssl: true
        es_enable_transport_ssl: true
        es_ssl_certificate_authority: "molecule/three_nodes_tls/test_certs/ca/ca.crt"
        es_ssl_key: "molecule/three_nodes_tls/test_certs/elasticsearch_node_2/elasticsearch_node_2.key"
        es_ssl_certificate: "molecule/three_nodes_tls/test_certs/elasticsearch_node_2/elasticsearch_node_2.crt"
        es_validate_certs: false
        es_config:
          cluster.name: "test-cluster"
          discovery.seed_hosts:
            - 172.18.0.2
            - 172.18.0.3
          http.host: "{{ es_network_host }}"
          http.port: 9200
          node.data: true
          node.master: false
          transport.host: "{{ es_network_host }}"
          transport.port: 9300
          bootstrap.memory_lock: false
```
