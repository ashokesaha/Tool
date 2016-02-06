import java.util.Arrays;
import java.util.List;

import com.citrix.netscaler.nitro.exception.nitro_exception;
import com.citrix.netscaler.nitro.resource.config.lb.lbvserver;
import com.citrix.netscaler.nitro.resource.config.ssl.sslcertkey;
import com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcertkey_binding;
import com.citrix.netscaler.nitro.resource.config.ssl.sslservice_sslcertkey_binding;
import com.citrix.netscaler.nitro.service.nitro_service;
import com.citrix.netscaler.nitro.resource.config.basic.service;
import com.citrix.netscaler.nitro.resource.config.basic.server;
import com.citrix.netscaler.nitro.resource.config.ssl.sslcipher_sslvserver_binding;
import com.citrix.netscaler.nitro.resource.config.ssl.sslvserver_sslcipher_binding;
import com.citrix.netscaler.nitro.resource.config.lb.lbvserver_service_binding;
import com.citrix.netscaler.nitro.resource.config.ssl.sslvserver;


public class Ashoke {

	public static void main(String[] args) {
		lbvserver						lbvserver_obj;
		sslcertkey						sslcertkey_obj;
		sslvserver_sslcertkey_binding	sslvserver_sslcertkey_binding_obj;
		sslservice_sslcertkey_binding	sslservice_sslcertkey_binding_obj;
		service							service_obj;
		server							server_obj;
		sslcipher_sslvserver_binding	sslcipher_sslvserver_binding_obj;
		sslvserver_sslcipher_binding	sslvserver_sslcipher_binding_obj;
		lbvserver_service_binding		lbvserver_service_binding_obj;
		sslvserver						sslvserver_obj;

		try {

			nitro_service ns_session = 
					new nitro_service("10.102.28.133","HTTP");

			ns_session.login("nsroot","nsroot");


			/******************************************************
			lbvserver_obj = new lbvserver();
			lbvserver_obj.set_name("vserver_1");
			lbvserver_obj.set_ipv46("10.102.28.134");
			lbvserver_obj.set_port(443);
			lbvserver_obj.set_servicetype("SSL");
			lbvserver.add(ns_session,lbvserver_obj);

			
			sslcertkey_obj = new sslcertkey();
			sslcertkey_obj.set_certkey("server_one");
			sslcertkey_obj.set_cert("server_one_cert.pem");
			sslcertkey_obj.set_key("server_one_key.pem");
			sslcertkey.add(ns_session,sslcertkey_obj);

			
			sslvserver_sslcertkey_binding_obj = new sslvserver_sslcertkey_binding();
			sslvserver_sslcertkey_binding_obj.set_vservername("vserver_1");
			sslvserver_sslcertkey_binding_obj.set_certkeyname("server_one");
			sslvserver_sslcertkey_binding.add(ns_session,
											sslvserver_sslcertkey_binding_obj);

			server_obj = new server();
			server_obj.set_ipaddress("10.102.28.61");
			server_obj.set_name("28_61");
			server.add(ns_session,server_obj);

			service_obj = new service();
			service_obj.set_name("svc_1");
			service_obj.set_servicetype("SSL");
			service_obj.set_servername("28_61");
			service_obj.set_port(443);
			service.add(ns_session,service_obj);


			sslcipher_sslvserver_binding_obj=new sslcipher_sslvserver_binding();
			sslcipher_sslvserver_binding_obj.set_vserver(true);
			sslcipher_sslvserver_binding_obj.set_vservername("vserver_1");
			sslcipher_sslvserver_binding_obj.set_cipheroperation("ADD");
			sslcipher_sslvserver_binding_obj.set_ciphgrpals("AES");
			sslcipher_sslvserver_binding.add(ns_session, sslcipher_sslvserver_binding_obj);

			sslvserver_sslcipher_binding_obj=new sslvserver_sslcipher_binding();
			sslvserver_sslcipher_binding_obj.set_vservername("vserver_1");
			sslvserver_sslcipher_binding_obj.set_ciphername("AES");
			sslvserver_sslcipher_binding.delete(ns_session,sslvserver_sslcipher_binding_obj);

			lbvserver_service_binding_obj = new lbvserver_service_binding();
			lbvserver_service_binding_obj.set_name("vserver_1");
			lbvserver_service_binding_obj.set_servicename("svc_1");
			lbvserver_service_binding.add(ns_session,lbvserver_service_binding_obj);


			lbvserver_service_binding_obj = new lbvserver_service_binding();
			lbvserver_service_binding_obj.set_name("vserver_1");
			lbvserver_service_binding_obj.set_servicename("svc_1");
			lbvserver_service_binding.delete(ns_session,lbvserver_service_binding_obj);


			sslcertkey_obj = new sslcertkey();
			sslcertkey_obj.set_certkey("client_one");
			sslcertkey_obj.set_cert("client_one_cert.pem");
			sslcertkey_obj.set_key("client_one_key.pem");
			sslcertkey.add(ns_session,sslcertkey_obj);


			sslservice_sslcertkey_binding_obj = new sslservice_sslcertkey_binding();
			sslservice_sslcertkey_binding_obj.set_servicename("svc_1");
			sslservice_sslcertkey_binding_obj.set_certkeyname("client_one");
			sslservice_sslcertkey_binding.add(ns_session,
											sslservice_sslcertkey_binding_obj);

			************************************************************/


			sslvserver_obj	=	new sslvserver();
			sslvserver_obj.set_vservername("vserver_1");
			sslvserver_obj.set_dh("ENABLED");
			sslvserver_obj.set_dhfile("dh_2048.pem");
			sslvserver.update(ns_session,sslvserver_obj);

		} catch(nitro_exception error) {
			System.out.println("NITRO Error -> Code " + error.getErrorCode() +
												" : " +error.getMessage());
		} catch(Exception e) {
			System.out.println("Java Error -> " +e.getMessage());
		}
	}
}
