package com.bjsasc.interface1;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.IOUtils;
import org.apache.http.impl.client.CloseableHttpClient;

import com.bjsasc.interface1.Base64;



/**
 * 不支持高可用，ossuri地址只能指定一个，仅仅可用于测试
 * @author oscar
 *
 */
public class OssTest {
	private static final String AUTH = "Authorization";
    private static final String DATE = "Date";
    private static final String BUCKETACL = "x-oss-acl";
    private static final String CONTENT_TYPE = "Content-Type";
    private static final String OSS_ACL = "x-oss-object-acl";
    private static final String POSITION = "position";
    
    private static final String ETAG = "ETag";
    private static final String STORETYPE = "x-oss-object-type";
    private static final String APPENDPOSITION = "x-oss-next-append-position";
    private static final String CONTENT_LENGTH = "Content-Length";
    private static final String CREATETIME = "Createtime";
    private static final String ACCESSTIME = "Accesstime";
    private static final String OSS_META = "oss-meta-";
    
//    private static String ossuri = "http://10.0.47.44:8080";
    private static String ossuri = "http://10.0.69.65:9090/oss";
//    private static String ossuri = "http://localhost:8080/oss";
    
//    private static String accessKey = "user1";
//	private static String securityKey = "618f6d14b121a0df7613d7e8a35b622e";
	// private static String accessKey = "gsl";
	// private static String securityKey = "40b311162824008e1753fbca1332a470";
	private static String accessKey = "bjm";
	private static String securityKey = "ac76c6454085b6bb7193bbf9e8b701ea";

	public static String authorization = null;
	
	static {
		try {
			authorization = new String(Base64.encode((accessKey + ":" + securityKey).getBytes("UTF-8")),"UTF-8");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	public enum Acl {
        ACL_DEFAULT, ACL_PUBLIC_READ_WRITER, ACL_PUBLIC_READ, ACL_PRIVATE
    }

	/**
     * 对应文档5.2.9。获取BucketInfo
     * @param bucket
     * @return
	 * @throws Exception 
     */
    public static int getBucketInfo(String bucket) throws Exception {
        String date = getDate();
        HttpURLConnection httpConnection = null;
        int code = 0;
        try {
            URL url = new URL(ossuri + "?bucketInfo&bucketName=" + URLEncoder.encode(bucket, "UTF-8"));
            httpConnection = (HttpURLConnection) url.openConnection();
            httpConnection.setRequestMethod("GET");
            httpConnection.setDoInput(true);
            httpConnection.setDoOutput(true);
            httpConnection.setRequestProperty(AUTH, authorization);
            httpConnection.setRequestProperty(DATE, date);
            httpConnection.connect();
            
            code = httpConnection.getResponseCode();
            System.out.println("code:" + code);
            
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (httpConnection != null)
                httpConnection.disconnect();
        }
        return code;
    }
    
    /**
     * 创建bucket
     * @param bucket
     * @return
     * @throws Exception
     */
    public static int putBucket(String bucket) throws Exception {
        return putBucket(bucket, (String) null);
    }
    
    /**
     * 创建bucket
     * @param bucket
     * @param acl
     * @return
     * @throws Exception
     */
    public static int putBucket(String bucket, String acl) throws Exception {
        String date = getDate();
        HttpURLConnection httpConnection = null;
        int code = 0;
        try {
            URL url = new URL(ossuri + "?bucketName=" + URLEncoder.encode(bucket, "UTF-8"));
            httpConnection = (HttpURLConnection) url.openConnection();
            httpConnection.setRequestMethod("PUT");
            httpConnection.setDoInput(true);
            httpConnection.setDoOutput(true);
            httpConnection.setRequestProperty(AUTH, authorization);
            httpConnection.setRequestProperty(DATE, date);
            if (acl != null) {
                httpConnection.setRequestProperty(BUCKETACL, acl);
            }
            httpConnection.setFixedLengthStreamingMode(0);
            httpConnection.connect();
            
            code = httpConnection.getResponseCode();
            System.out.println("code:" + code);
            
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (httpConnection != null)
                httpConnection.disconnect();
        }
        return code;
    }
    
    /**
     * 创建oject对象
     * 
     * @param bucket
     * @param object
     * @param acl
     * @param metas
     * @param contentType
     * @param contentLength
     * @param is
     * @return
     * @throws OssException
     */
    public static int putObject(String bucket, String object, Acl acl, Map<String, String> metas,
            String contentType, long contentLength, InputStream is) throws Exception {
    	if(object == null || object.length()==0) {
    		return 404;
    	}
        String date = getDate();
        HttpURLConnection httpConnection = null;
        OutputStream os = null;
        int code = 0;
        try {
        	URL url = new URL(ossuri + "/" + getObjectInUrl(object) + "?bucketName=" + URLEncoder.encode(bucket, "UTF-8"));
            httpConnection = (HttpURLConnection) url.openConnection();
            httpConnection.setRequestMethod("PUT");
            httpConnection.setDoInput(true);
            httpConnection.setDoOutput(true);
            httpConnection.setRequestProperty(AUTH, authorization);
            httpConnection.setRequestProperty(DATE, date);
            httpConnection.setFixedLengthStreamingMode(contentLength);
        	
            if (contentType != null)
                httpConnection.setRequestProperty(CONTENT_TYPE, contentType);
            if (acl != null)
                httpConnection.setRequestProperty(OSS_ACL, acl.ordinal() + "");
            if (metas != null) {
                for (Map.Entry<String, String> e : metas.entrySet()) {
                    httpConnection.setRequestProperty(e.getKey(), e.getValue());
                }
            }
            httpConnection.connect();
            os = httpConnection.getOutputStream();
            if (is != null) {
                writeData(is, os);
                os.flush();
            }

            code = httpConnection.getResponseCode();
            System.out.println("code:" + code);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (os != null && is != null)
                try {
                    is.close();
                    os.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            if (httpConnection != null)
                httpConnection.disconnect();
        }
        return code;
    }
    
    /**
     * 获取对象
     * 
     * @param bucket
     * @param object
     * @return
     * @throws OssException
     */
    public static int getObject(String bucket, String object) throws Exception {
        String date = getDate();
        HttpURLConnection httpConnection = null;
        InputStream is = null;
        int code = 0;
        try {
            URL url = new URL(ossuri + "/" + getObjectInUrl(object) + "?bucketName=" + URLEncoder.encode(bucket, "UTF-8"));
            httpConnection = (HttpURLConnection) url.openConnection();
            httpConnection.setRequestMethod("GET");
            httpConnection.setDoInput(true);
            httpConnection.setDoOutput(true);
            httpConnection.setRequestProperty(AUTH, authorization);
            httpConnection.setRequestProperty(DATE, date);
            httpConnection.connect();
            
            code = httpConnection.getResponseCode();
            System.out.println("code:" + code);

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (is != null)
                try {
                    is.close();
                } catch (IOException ie) {
                    ie.printStackTrace();
                }
            if (httpConnection != null)
                httpConnection.disconnect();
        }
        return code;
    }
    
    /**
     * 获取对象
     * 
     * @param bucket
     * @param object
     * @return
     * @throws OssException
     */
    public static int getObject(String bucket, String object, File downFile) throws Exception {
        String date = getDate();
        HttpURLConnection httpConnection = null;
        InputStream is = null;
        FileOutputStream output = null;
        int code = 0;
        try {
            URL url = new URL(ossuri + "/" + getObjectInUrl(object) + "?bucketName=" + URLEncoder.encode(bucket, "UTF-8"));
            httpConnection = (HttpURLConnection) url.openConnection();
            httpConnection.setRequestMethod("GET");
            httpConnection.setDoInput(true);
            httpConnection.setDoOutput(true);
            httpConnection.setRequestProperty(AUTH, authorization);
            httpConnection.setRequestProperty(DATE, date);
            httpConnection.connect();
            
            code = httpConnection.getResponseCode();
            System.out.println("code:" + code);
            
            if (code == 200) {
                is = httpConnection.getInputStream();
                output = new FileOutputStream(downFile);
                writeData(is, output);
            }

        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (is != null)
                try {
                	output.close();
                    is.close();
                } catch (IOException ie) {
                    ie.printStackTrace();
                }
            if (httpConnection != null)
                httpConnection.disconnect();
        }
        return code;
    }
    
    /**
     * 删除对象
     * 
     * @param bucket
     * @param object
     * @throws OssException
     */
    public static int deleteObject(String bucket, String object) throws Exception {
    	if(object == null || object.length() ==0 ) {
    		return 404;
    	}
        String date = getDate();
        HttpURLConnection httpConnection = null;
        int code = 0;
        try {
            URL url = new URL(ossuri + "/" + getObjectInUrl(object) + "?bucketName=" + URLEncoder.encode(bucket, "UTF-8"));
            httpConnection = (HttpURLConnection) url.openConnection();
            httpConnection.setRequestMethod("DELETE");
            httpConnection.setDoInput(true);
            httpConnection.setDoOutput(true);
            httpConnection.setRequestProperty(AUTH, authorization);
            httpConnection.setRequestProperty(DATE, date);
            httpConnection.connect();
            
            code = httpConnection.getResponseCode();
            System.out.println("code:" + code);
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (httpConnection != null)
                httpConnection.disconnect();
        }
        return code;
    }
    
    private static String getDate() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
        Date date = new Date();
        return sdf.format(date);
    }
    
    private static void writeData(InputStream is, OutputStream os) throws IOException {
        byte[] b = new byte[4096];
        int len = 0;
        while ((len = is.read(b)) > 0) {
            os.write(b, 0, len);
        }
    }
    
    private static String getObjectInUrl(String path) {
        String objectRebuild = "";
        try {
            path = path.replace('/', '|');
            objectRebuild = URLEncoder.encode(path, "UTF-8");
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
        return objectRebuild;
    }
    
    /**
     * 创建可追加的oject对象
     * 
     * @param bucket
     * @param object
     * @param acl
     * @param metas
     * @param contentType
     * @param contentLength
     * @param is
     * @return
     * @throws OssException
     */
    public static int appendObject(String bucket, String object, Acl acl, Map<String, String> metas,
            String contentType, long contentLength, InputStream is, long position) throws Exception {
        String date = getDate();
        HttpURLConnection httpConnection = null;
        OutputStream os = null;
        HashMap<String, String> map = new HashMap<String, String>();
        int code = 0;
        try {
            map.put(POSITION, String.valueOf(position));
            String appendUrl = ossuri + "/" + getObjectInUrl(object) + "?append&bucketName=" + bucket;
            String path = appendParameter(appendUrl, map, false);
            URL url = new URL(path);
            httpConnection = (HttpURLConnection) url.openConnection();
            httpConnection.setRequestMethod("POST");
            httpConnection.setDoInput(true);
            httpConnection.setDoOutput(true);
            httpConnection.setRequestProperty(AUTH, authorization);
            httpConnection.setRequestProperty(DATE, date);
            httpConnection.setFixedLengthStreamingMode(contentLength);
            
            if (contentType != null)
                httpConnection.setRequestProperty(CONTENT_TYPE, contentType);
            if (acl != null)
                httpConnection.setRequestProperty(OSS_ACL, acl.ordinal() + "");
            if (metas != null) {
                for (Map.Entry<String, String> e : metas.entrySet()) {
                    httpConnection.setRequestProperty(e.getKey(), e.getValue());
                }
            }
            httpConnection.connect();
            os = httpConnection.getOutputStream();
            if (is != null) {
                writeData(is, os);
                os.flush();
            }

            code = httpConnection.getResponseCode();
            
        } catch (Exception e) {
        	e.printStackTrace();
        } finally {
            if (os != null && is != null)
                try {
                    is.close();
                    os.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            if (httpConnection != null)
                httpConnection.disconnect();
        }
        return code;
    }
    
    private static String appendParameter(String url, HashMap<String, String> map, boolean firstFlag) throws Exception {
        boolean isFirst = firstFlag;
        for (Map.Entry<String, String> entry : map.entrySet()) {
            String key = entry.getKey();
            String value = entry.getValue();
            if (key != null && !key.equals("") && value != null ) {
                if (isFirst) {
                    url = url + "?" + key + "=" + URLEncoder.encode(value, "UTF-8");
                    isFirst = false;
                } else {
                    url = url + "&" + key + "=" + URLEncoder.encode(value, "UTF-8");
                }

            }
        }
        return url;
    }
    
    public static int headObject(String bucket, String object, HashMap<String, String> map) throws Exception {
        String date = getDate();
        HttpURLConnection httpConnection = null;
        int code = -1;
        try {
            URL url = new URL(ossuri + "/" + getObjectInUrl(object) + "?bucketName=" + bucket);
            System.out.println(url + "===");
            httpConnection = (HttpURLConnection) url.openConnection();
            httpConnection.setRequestMethod("HEAD");
            httpConnection.setDoInput(true);
            httpConnection.setDoOutput(true);
            httpConnection.setRequestProperty(AUTH, authorization);
            httpConnection.setRequestProperty(DATE, date);

            httpConnection.connect();
            code = httpConnection.getResponseCode();
            if (code == 204) {
                Map<String, List<String>> retHeads = httpConnection.getHeaderFields();
                for (Map.Entry<String, List<String>> e : retHeads.entrySet()) {
                    String key = e.getKey();
                    if (key != null && (key.equals(ETAG) || key.equals(STORETYPE)|| key.equals(CONTENT_TYPE) || key.equals(APPENDPOSITION)
                            || key.equals(CONTENT_LENGTH) || key.equals(CREATETIME) || key.equals(ACCESSTIME)
                            || key.indexOf(OSS_META) == 0)) {
                        map.put(key, e.getValue().get(0));
                    }
                }
            }
            
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (httpConnection != null)
                httpConnection.disconnect();
        }
        return code;
    }
    
    public static Long getAppendObjectLenth(String bucketName, String objectname) {
    	HashMap<String, String> map = new HashMap<String, String>();
    	try {
			int result = headObject(bucketName, objectname, map);
		} catch (Exception e) {
			e.printStackTrace();
		}
    	Long lenth = Long.valueOf(map.get(CONTENT_LENGTH));
    	return lenth;
    }
    
    public static String getDownloadPath(String bucket, String objectName) {
        String date = getDate();
        HttpURLConnection httpConnection = null;
        InputStream is = null;
        String downloadpath = "";
        try {
            HashMap<String, String> map = new HashMap<>();
            map.put("objectName", objectName);
            map.put("bucketName", bucket);
            String path = appendParameter(ossuri + "/generDownloadPath", map, true);

            URL url = new URL(path);
            httpConnection = (HttpURLConnection) url.openConnection();
            httpConnection.setRequestMethod("GET");
            httpConnection.setDoInput(true);
            httpConnection.setDoOutput(true);
            httpConnection.setRequestProperty(AUTH, authorization);
            httpConnection.setRequestProperty(DATE, date);

            httpConnection.connect();
            int code = httpConnection.getResponseCode();
            
            if (code != 200) {
            	return null;
			}
            InputStream inputStream = httpConnection.getInputStream();
            downloadpath = IOUtils.toString(inputStream,"utf-8");
            return downloadpath;
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            if (is != null)
                try {
                    is.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            if (httpConnection != null)
                httpConnection.disconnect();
        }
		return downloadpath;
    }
    
}
