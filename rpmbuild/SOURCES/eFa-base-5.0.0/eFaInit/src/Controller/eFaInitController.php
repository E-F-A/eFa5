<?php
// src/AppBundle/Controller/eFaInitController.php
namespace App\Controller;

use App\Entity\eFaInitTask;
use App\Entity\passwordCompareTask;
use App\Form\LanguageTaskType;
use App\Form\LanguageEditTaskType;
use App\Form\YesNoTaskType;
use App\Form\YesNoEditTaskType;
use App\Form\TextboxTaskType;
use App\Form\TextboxEditTaskType;
use App\Form\PasswordTaskType;
use App\Form\PasswordEditTaskType;
use App\Form\TimezoneTaskType;
use App\Form\TimezoneEditTaskType;
use App\Form\VerifySettingsTaskType;
use App\Form\InterfaceTaskType;
use App\Form\InterfaceEditTaskType;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\Session\SessionInterface;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Validator\Validator\ValidatorInterface;
use Symfony\Component\Routing\Attribute\Route;

class eFaInitController extends AbstractController
{
    protected $timeout=900;

    private $validator;

    public function __construct(ValidatorInterface $validator)
    {
        $this->validator = $validator;
    }

    #[Route("/{_locale}",
          name: "languagepage",
          defaults: ["edit" => null]
      )]
    #[Route("/{_locale}/{edit}",
          name: "languageeditpage",
          requirements: ["edit" => "edit"]
      )]
    public function indexAction(Request $request, $edit, SessionInterface $session)
    {
        $task = new eFaInitTask();

        if ($edit === "edit") { 
            $form = $this->createForm(LanguageEditTaskType::class, $task, array('locale' => $request->getLocale()));
        } else {
            $form = $this->createForm(LanguageTaskType::class, $task, array('locale' => $request->getLocale()));
        }

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $task = $form->getData();

            $session->set('locale', $task->getLanguage()); 

            if ($edit === "edit") {
                return $this->redirectToRoute('verifysettingspage', array('_locale' => $task->getLanguage(), 'slug' => 'verify'));
            } else {
                return $this->redirectToRoute('textboxpage', array('_locale' => $task->getLanguage(), 'slug' => 'hostname'));
            }
        }
        if ($edit === "edit") {
            return $this->render('languageedit/index.html.twig', array(
                'form' => $form->createView(),
            ));
        } else { 
            return $this->render('language/index.html.twig', array(
                'form' => $form->createView(),
            ));
        }
    }

    
    #[Route("/")]
    public function localeAction(Request $request) 
    {
        $clientLocale = strtolower(str_split($_SERVER['HTTP_ACCEPT_LANGUAGE'], 2)[0]);
        switch ($clientLocale) {
        case 'fr':
            return $this->redirectToRoute('languagepage', array('_locale' => 'fr'));
        break;
        case 'da':
            return $this->redirectToRoute('languagepage', array('_locale' => 'da'));
        break;
        case 'de':
            return $this->redirectToRoute('languagepage', array('_locale' => 'de'));
        break;
        case 'nl':
            return $this->redirectToRoute('languagepage', array('_locale' => 'nl'));
        break;
        case 'zh_CN':
            return $this->redirectToRoute('languagepage', array('_locale' => 'zh_CN'));
        break;
        case 'zh_TW':
            return $this->redirectToRoute('languagepage', array('_locale' => 'zh_TW'));
        break;
        case 'pt_PT':
            return $this->redirectToRoute('languagepage', array('_locale' => 'pt_PT'));
        break;
        case 'tr':
            return $this->redirectToRoute('languagepage', array('_locale' => 'tr'));
        break;
        case 'sv':
            return $this->redirectToRoute('languagepage', array('_locale' => 'sv'));
        break;
        case 'ru':
            return $this->redirectToRoute('languagepage', array('_locale' => 'ru'));
        break;
        case 'cz':
            return $this->redirectToRoute('languagepage', array('_locale' => 'cz'));
        break;
        case 'el':
            return $this->redirectToRoute('languagepage', array('_locale' => 'el'));
        break;
        case 'it':
            return $this->redirectToRoute('languagepage', array('_locale' => 'it'));
        break;
        case 'no':
            return $this->redirectToRoute('languagepage', array('_locale' => 'no'));
        break;
        default:
            return $this->redirectToRoute('languagepage', array('_locale' => 'en'));
        break;
        }
    }

    
    #[Route("/{_locale}/{slug}",
          name: "textboxpage",
          requirements: ["slug" => "hostname|domainname|email|ipv4address|ipv4netmask|ipv4gateway|ipv6address|ipv6prefix|ipv6gateway|dns1|dns2|webusername|cliusername|mailserver|orgname"],
          defaults: ["edit" => null]
      )]
    #[Route("/{_locale}/{slug}/{edit}",
          name: "textboxeditpage",
          requirements: ["slug" => "hostname|domainname|email|ipv4address|ipv4netmask|ipv4gateway|ipv6address|ipv6prefix|ipv6gateway|dns1|dns2|webusername|cliusername|mailserver|orgname", "edit" => "edit"]
      )]
    public function textboxAction(Request $request, $edit, $slug, SessionInterface $session)
    {
        $task = new eFaInitTask();

        switch ($slug) 
        {
            case "hostname":
                $options = array(
                    'varLabel'    => 'Please enter a hostname',
                    'varProperty' => 'Hostname',
                    'varData'     => $session->get($slug),
                );
                $varTitle     = 'Hostname';
                $nextSlug     = 'domainname';
                $nextPage     = 'textboxpage';
                $previousSlug = 'language';
                $previousPage = 'languagepage';
            break;
            case "domainname":
                $options = array(
                    'varLabel'    => 'Please enter a domain name',
                    'varProperty' => 'Domainname',
                    'varData'     => $session->get($slug),
                );
                $varTitle     = 'Domain Name';
                $nextSlug     = 'email';
                $nextPage     = 'textboxpage';
                $previousSlug = 'hostname';
                $previousPage = 'textboxpage';
            break;
            case "email":
                $options = array(
                    'varLabel'    => 'Please enter an email address for important notifications',
                    'varProperty' => 'Email',
                    'varData'     => $session->get($slug),
                );
                $varTitle     = 'Email';
                $nextSlug     = 'interface';
                $nextPage     = 'interfacepage';
                $previousSlug = 'domainname';
                $previousPage = 'textboxpage';
            break;
            case "ipv4address":
                $options = array(
                    'varLabel'    => 'Please enter a valid IPv4 address',
                    'varProperty' => 'IPv4address',
                    'varData'     => $session->get($slug),
                );
                if ($options['varData'] === '' || $options['varData'] === null) {
                    try {
                        $interface = $session->get('interface');
                        $process = Process::fromShellCommandline("ip add show dev $interface | grep inet\  | grep -v inet\ 127. | awk '{print $2}' | awk -F'/' '{print $1}'");
                        $process->mustRun();
                        $options['varData'] = $process->getOutput();
                    } catch (ProcessFailedException $exception) {
                        $options['varData'] = '';
                    } 
                }
                $varTitle     = 'IPv4 Address';
                $nextSlug     = 'ipv4netmask';
                $nextPage     = 'textboxpage';
                $previousSlug = 'configipv4';
                $previousPage = 'yesnopage';
            break;
            case "ipv4netmask":
                $options = array(
                    'varLabel'    => 'Please enter a valid IPv4 netmask length',
                    'varProperty' => 'IPv4netmask',
                    'varData'     => $session->get($slug),
                );

                if ($options['varData'] === '' || $options['varData'] === null) {
                    try {
                        $interface = $session->get('interface');
                        $process = Process::fromShellCommandline("ip add show dev $interface | grep inet\  | grep -v inet\ 127. | awk '{print $2}' | awk -F'/' '{print $2}'");
                        $process->mustRun();
                        $options['varData'] = $process->getOutput();
                    } catch (ProcessFailedException $exception) {
                        $options['varData'] = '';
                    } 
                }

                $varTitle     = 'IPv4 Netmask';
                $nextSlug     = 'ipv4gateway';
                $nextPage     = 'textboxpage';
                $previousSlug = 'ipv4address';
                $previousPage = 'textboxpage';
            break;
            case "ipv4gateway":
                $options = array(
                    'varLabel'    => 'Please enter a valid IPv4 gateway',
                    'varProperty' => 'IPv4gateway',
                    'varData'     => $session->get($slug),
                );

                if ($options['varData'] === '' || $options['varData'] === null) {
                    try {
                        $interface = $session->get('interface');
                        $process = Process::fromShellCommandline("ip -4 route list default dev $interface | awk {'print $3'}");
                        $process->mustRun();
                        $options['varData'] = $process->getOutput();
                    } catch (ProcessFailedException $exception) {
                        $options['varData'] = '';
                    } 
                }

                $varTitle     = 'IPv4 Gateway';
                $nextSlug     = 'ipv6dns';
                $nextPage     = 'yesnopage';
                $previousSlug = 'ipv4netmask';
                $previousPage = 'textboxpage';
            break;
             case "ipv6address":
                $options = array(
                    'varLabel'    => 'Please enter a valid IPv6 address',
                    'varProperty' => 'IPv6address',
                    'varData'     => $session->get($slug),
                );

                if ($options['varData'] === '' || $options['varData'] === null) {
                    try {
                        $interface = $session->get('interface');
                        $process = Process::fromShellCommandline("ip add show dev $interface | grep inet6 | grep -v inet6\ ::1 | grep global | awk '{print $2}' | awk -F'/' '{print $1}'");
                        $process->mustRun();
                        $options['varData'] = $process->getOutput();
                    } catch (ProcessFailedException $exception) {
                        $options['varData'] = '';
                    } 
                }

                $varTitle     = 'IPv6 Address';
                $nextSlug     = 'ipv6prefix';
                $nextPage     = 'textboxpage';
                $previousSlug = 'configipv6';
                $previousPage = 'yesnopage';
            break;
            case "ipv6prefix":
                $options = array(
                    'varLabel'    => 'Please enter a valid IPv6 prefix',
                    'varProperty' => 'IPv6prefix',
                    'varData'     => $session->get($slug),
                );

                if ($options['varData'] === '' || $options['varData'] === null) {
                    try {
                        $interface = $session->get('interface');
                        $process = Process::fromShellCommandline("ip add show $interface | grep inet6\ | grep global | awk '{print $2}' | awk -F'/' '{print $2}'");
                        $process->mustRun();
                        $options['varData'] = $process->getOutput();
                    } catch (ProcessFailedException $exception) {
                        $options['varData'] = '';
                    } 
                }

                $varTitle     = 'IPv6 Prefix';
                $nextSlug     = 'ipv6gateway';
                $nextPage     = 'textboxpage';
                $previousSlug = 'ipv6address';
                $previousPage = 'textboxpage';
            break;
            case "ipv6gateway":
                $options = array(
                    'varLabel'    => 'Please enter a valid IPv6 gateway',
                    'varProperty' => 'IPv6gateway',
                    'varData'     => $session->get($slug),
                );

                if ($options['varData'] === '' || $options['varData'] === null) {
                    try {
                        $interface = $session->get('interface');
                        $process = Process::fromShellCommandline("ip -6 route list default dev $interface | awk {'print $3'}");
                        $process->mustRun();
                        $options['varData'] = $process->getOutput();
                    } catch (ProcessFailedException $exception) {
                        $options['varData'] = '';
                    } 
                }

                $varTitle     = 'IPv6 Gateway';
                $nextSlug     = 'configrecursion';
                $nextPage     = 'yesnopage';
                $previousSlug = 'ipv6prefix';
                $previousPage = 'textboxpage';
            break;
            case "dns1":
                $options = array(
                    'varLabel'    => 'Please enter the primary DNS address',
                    'varProperty' => 'DNS1',
                    'varData'     => $session->get($slug),
                );

                if ($options['varData'] === '' || $options['varData'] === null) {
                    try {
                        $process = Process::fromShellCommandline("grep nameserver /etc/resolv.conf | awk '{print $2}' | sed -n 1p");
                        $process->mustRun();
                        $options['varData'] = $process->getOutput();
                    } catch (ProcessFailedException $exception) {
                        $options['varData'] = '';
                    } 
                }

                $varTitle     = 'Primary DNS';
                $nextSlug     = 'dns2';
                $nextPage     = 'textboxpage';
                $previousSlug = 'configrecursion';
                $previousPage = 'yesnopage';
            break;
            case "dns2":
                $options = array(
                    'varLabel'    => 'Please enter the secondary DNS address',
                    'varProperty' => 'DNS2',
                    'varData'     => $session->get($slug),
                );

                if ($options['varData'] === '' || $options['varData'] === null) {
                    try {
                        $process = Process::fromShellCommandline("grep nameserver /etc/resolv.conf | awk '{print $2}' | sed -n 2p");
                        $process->mustRun();
                        $options['varData'] = $process->getOutput();
                    } catch (ProcessFailedException $exception) {
                        $options['varData'] = '';
                    } 
                }

                $varTitle     = 'Secondary DNS';
                $nextSlug     = 'webusername';
                $nextPage     = 'textboxpage';
                $previousSlug = 'dns1';
                $previousPage = 'textboxpage';
            break;
            case "webusername":
                $options = array(
                    'varLabel'    => 'Please enter the username for the admin web interface',
                    'varProperty' => 'Webusername',
                    'varData'     => $session->get($slug),
                );
                $varTitle     = 'Web Admin Username';
                $nextSlug     = 'webpassword';
                $nextPage     = 'passwordpage';
                $previousSlug = 'configrecursion';
                $previousPage = 'yesnopage';
            break;
            case "cliusername":
                $options = array(
                    'varLabel'    => 'Please enter the username for the admin console interface',
                    'varProperty' => 'CLIusername',
                    'varData'     => $session->get($slug),
                );
                $varTitle     = 'Console Admin Username';
                $nextSlug     = 'clipassword';
                $nextPage     = 'passwordpage';
                $previousSlug = 'webpassword';
                $previousPage = 'passwordpage';
            break;
            case "mailserver":
                $options = array(
                    'varLabel'    => 'Please enter the IP or hostname of the local mail server',
                    'varProperty' => 'Mailserver',
                    'varData'     => $session->get($slug),
                );
                $varTitle     = 'Local Mail Server';
                $nextSlug     = 'orgname';
                $nextPage     = 'textboxpage';
                $previousSlug = 'timezone';
                $previousPage = 'timezonepage';
            break;
            case "orgname":
                $options = array(
                    'varLabel'    => 'Please enter your organization name (No spaces, dots, or underscores)',
                    'varProperty' => 'Orgname',
                    'varData'     => $session->get($slug),
                );
                $varTitle     = 'Organization Name';
                $nextSlug     = 'verify';
                $nextPage     = 'verifysettingspage';
                $previousSlug = 'mailserver';
                $previousPage = 'textboxpage';
            break;

        }

        if ($edit === 'edit') {
            $form = $this->createForm(TextboxEditTaskType::class, $task, $options);
        } else { 
            $form = $this->createForm(TextboxTaskType::class, $task, $options);
        }

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $task = $form->getData();

            $getMethod = "get" . $slug;
            $session->set($slug, $task->$getMethod());
            if ($edit === 'edit') {
                $action = 'verify';
                $page   = 'verifysettingspage';
            } else {
                $action = $form->get('Next')->isClicked() || $form->get('NextHidden')->isClicked() ? $nextSlug : $previousSlug;
                $page   = $form->get('Next')->isClicked() || $form->get('NextHidden')->isClicked() ? $nextPage : $previousPage;
            }

            return $this->redirectToRoute($page, array('_locale' => $request->getLocale(), 'slug' => $action));
        }
        
        if ($edit === 'edit') {
            return $this->render('textboxedit/index.html.twig', array(
                'form' => $form->createView(),
                'title' => $varTitle
            ));
        } else {
            return $this->render('textbox/index.html.twig', array(
                'form' => $form->createView(),
                'title' => $varTitle
            ));
        }
    }


    
    #[Route("/{_locale}/{slug}",
          name: "interfacepage",
          requirements: ["slug" => "interface"],
          defaults: ["edit" => null]
      )]
    #[Route("/{_locale}/{slug}/{edit}",
          name: "interfaceeditpage",
          requirements: ["slug" => "interface", "edit" => "edit"]
      )]
    public function interfaceAction(Request $request, $edit, $slug, SessionInterface $session)
    {
        $task = new eFaInitTask();

        $options = array(
            'varProperty' => 'Interface',
        );
        $varLabel     = 'Please choose your interface';
        $nextSlug     = 'configipv4';
        $nextPage     = 'yesnopage';
        $previousSlug = 'email';
        $previousPage = 'textboxpage';
        try {
            $process = Process::fromShellCommandline("ip link show | grep ^[0-9] | awk -F': ' '{print $2}' | sed -e '/^lo/d' -e 's/@.*$//g' | sort | uniq");
            $process->mustRun();
            foreach ( explode("\n",$process->getOutput()) as $var ) 
            {
                if ( trim($var) !== '') {
                    $options['varChoices'][trim($var)] = trim($var);
                }
            }
        } catch (ProcessFailedException $exception) {
               $options['varChoices']['eth0'] = 'eth0';
        }
        if ($edit === 'edit') {
            $form = $this->createForm(InterfaceEditTaskType::class, $task, $options);
        } else {
            $form = $this->createForm(InterfaceTaskType::class, $task, $options);
        }

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $task = $form->getData();

            $session->set('interface', $task->getInterface()); 

            if ($edit === 'edit') {
                $action = 'verify';
                $page   = 'verifysettingspage';
            } else {
                $action = $form->get('Next')->isClicked() || $form->get('NextHidden')->isClicked() ? $nextSlug : $previousSlug;
                $page   = $form->get('Next')->isClicked() || $form->get('NextHidden')->isClicked() ? $nextPage : $previousPage;
            }
            
            return $this->redirectToRoute($page, array('_locale' => $request->getLocale(), 'slug' => $action));

       }
        if ($edit === "edit") {
            return $this->render('interfaceedit/index.html.twig', array(
                'form' => $form->createView(),
                'label' => $varLabel,
            ));
        } else { 
            return $this->render('interface/index.html.twig', array(
                'form' => $form->createView(),
                'label' => $varLabel,
            ));
        }
    }


    
    #[Route("/{_locale}/{slug}",
          name: "yesnopage",
          requirements: ["slug" => "configipv4|ipv6dns|configipv6|configrecursion|configvirtual|configutc"],
          defaults: ["edit" => null]
      )]
    #[Route("/{_locale}/{slug}/{edit}",
          name: "yesnoeditpage",
          requirements: ["slug" => "configipv4|ipv6dns|configipv6|configrecursion|configvirtual|configutc","edit" => "edit"]
      )]
    public function yesnoAction(Request $request, $slug, $edit, SessionInterface $session)
    {
        if ($edit === 'edit') {
            $form = $this->createForm(YesNoEditTaskType::class);
        } else {
            $form = $this->createForm(YesNoTaskType::class);
        }

        switch($slug) 
        {
            case "configipv4":
                $varTitle     = 'Configure IPv4';
                $varQuestion  = 'Do you want to set a static IPv4 address?';
                $yesSlug      = 'ipv4address';
                $yesPage      = 'textboxpage';
                $noSlug       = 'ipv6dns';
                $noPage       = 'yesnopage';
                $previousPage = 'interfacepage';
                $previousSlug = 'interface';
            break;
            case "ipv6dns":
                $varTitle     = 'Enable IPv6 DNS';
                $varQuestion  = 'Do you want to Enable IPv6 DNS?';
                $yesSlug      = 'configipv6';
                $yesPage      = 'yesnopage';
                $noSlug       = 'configipv6';
                $noPage       = 'yesnopage';
                $previousPage = 'yesnopage';
                $previousSlug = 'configipv4';
            break;
            case "configipv6":
                $varTitle     = 'Configure IPv6';
                $varQuestion  = 'Do you want to set a static IPv6 address?';
                $yesSlug      = 'ipv6address';
                $yesPage      = 'textboxpage';
                $noSlug       = 'configrecursion';
                $noPage       = 'yesnopage';
                $previousPage = 'yesnopage';
                $previousSlug = 'ipv6dns';
            break;
            case "configrecursion":
                $varTitle     = 'Configure DNS Recursion';
                $varQuestion  = 'Do you want to enable full DNS Recursion?';
                $yesSlug      = 'webusername';
                $yesPage      = 'textboxpage';
                $noSlug       = 'dns1';
                $noPage       = 'textboxpage';
                $previousPage = 'yesnopage';
                $previousSlug = 'configipv6';
            break;
            case "configvirtual":
                $varTitle     = 'Configure Hypervisor Tools';
                $varQuestion  = 'Do you want to install hypervisor tools for your hypervisor?';
                $yesSlug      = 'configutc';
                $yesPage      = 'yesnopage';
                $noSlug       = 'configutc';
                $noPage       = 'yesnopage';
                $previousPage = 'passwordpage';
                $previousSlug = 'clipassword';
            break;
            case "configutc":
                $varTitle     = 'Configure UTC Time';
                $varQuestion  = 'Is the host set to UTC time?';
                $yesSlug      = 'timezone';
                $yesPage      = 'timezonepage';
                $noSlug       = 'timezone';
                $noPage       = 'timezonepage';
                $previousPage = 'yesnopage';
                $previousSlug = 'configvirtual';
            break;
        }

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            if ($edit === 'edit') {
                if ($form->get('Return')->isClicked()) {
                    $action = 'verifysettingspage';
                    $slug   = 'verify';
                } elseif ($form->get('Yes')->isClicked()) {
                    $session->set($slug, '1');
                    $action = 'verifysettingspage';
                    $slug   = 'verify';
                } else {
                   $session->set($slug, '0');
                   $action = 'verifysettingspage';
                   $slug   = 'verify';
                }
           } else {
                if ($form->get('Back')->isClicked()) {
                    $action = $previousPage;
                   $slug   = $previousSlug;
                } elseif ($form->get('Yes')->isClicked()) {
                    $session->set($slug, '1');
                    $action = $yesPage;
                    $slug   = $yesSlug;
                } else {
                   $session->set($slug, '0');
                   $action = $noPage;
                   $slug   = $noSlug;
                }
           }

            return $this->redirectToRoute($action, array('_locale' => $request->getLocale(), 'slug' => $slug));
        }
        if ($edit === 'edit') {
            return $this->render('yesnoedit/index.html.twig', array(
                'form' => $form->createView(),
                'title' => $varTitle,
                'question' => $varQuestion
                ));
        } else {
            return $this->render('yesno/index.html.twig', array(
                'form' => $form->createView(),
                'title' => $varTitle,
                'question' => $varQuestion
                ));
        }
    }

    
    #[Route("/{_locale}/{slug}",
          name: "passwordpage",
          requirements: ["slug" => "webpassword|clipassword"],
          defaults: ["edit" => null]
      )]
    #[Route("/{_locale}/{slug}/{edit}",
          name: "passwordeditpage",
          requirements: ["slug" => "webpassword|clipassword", "edit" => "edit"]
      )]
    public function passwordAction(Request $request, $slug, $edit, SessionInterface $session)
    {
        $task = new eFaInitTask();

        switch ($slug) 
        {
            case "webpassword":
                $options = array(
                    'varLabel1'    => 'Please enter the web admin password',
                    'varLabel2'    => 'Please re-enter the web admin password',
                    'varProperty1' => 'Webpassword1',
                    'varProperty2' => 'Webpassword2',
                );
                $varTitle     = 'Web Admin Password';
                $nextSlug     = 'cliusername';
                $nextPage     = 'textboxpage';
                $previousSlug = 'webusername';
                $previousPage = 'textboxpage';
            break;
            case "clipassword":
                $options = array(
                    'varLabel1'    => 'Please enter the console admin password',
                    'varLabel2'    => 'Please re-enter the console admin password',
                    'varProperty1' => 'CLIpassword1',
                    'varProperty2' => 'CLIpassword2',
                );
                $varTitle     = 'Console Admin Password';
                $nextSlug     = 'configvirtual';
                $nextPage     = 'yesnopage';
                $previousSlug = 'cliusername';
                $previousPage = 'textboxpage';
            break;

        }
        if ($edit === 'edit') {
             $form = $this->createForm(PasswordEditTaskType::class, $task, $options);
        } else {
             $form = $this->createForm(PasswordTaskType::class, $task, $options);
        }

        $form->handleRequest($request);

        if ($form->isSubmitted() && $form->isValid()) {
            $task = $form->getData();

            $getMethod = "get" . $options['varProperty1'];
            $session->set($slug, $task->$getMethod());
            
            $passwordcompare = new passwordCompareTask();
            $passwordcompare->setPassword1($session->get('webpassword'));
            $passwordcompare->setPassword2($session->get('clipassword'));
            
            $errors = $this->validator->validate($passwordcompare);

            if (count($errors) === 0) {
                if ($edit === 'edit') {
                   $action = 'verify';
                   $page   = 'verifysettingspage';
                } else {
                    $action = $form->get('Next')->isClicked() || $form->get('NextHidden')->isClicked() ? $nextSlug : $previousSlug;
                    $page   = $form->get('Next')->isClicked() || $form->get('NextHidden')->isClicked() ? $nextPage : $previousPage;
                }

                return $this->redirectToRoute($page, array('_locale' => $request->getLocale(), 'slug' => $action));
            } elseif (!($form->get('Next')->isClicked() || $form->get('NextHidden')->isClicked())) {
                return $this->redirectToRoute($previousPage, array('_locale' => $request->getLocale(), 'slug' => $previousSlug));
            } else {
                if ($edit === 'edit') {
                    return $this->render('passwordeditbox/index.html.twig', array(
                        'form' => $form->createView(),
                        'error' => 'Web and ClI Passwords cannot match',
                        'title' => $varTitle,
                    ));
                } else {
                    return $this->render('passwordbox/index.html.twig', array(
                        'form' => $form->createView(),
                        'error' => 'Web and CLI Passwords cannot match',
                        'title' => $varTitle,
                    ));
                }
            }
        }
        
        if ($edit === 'edit') {
            return $this->render('passwordeditbox/index.html.twig', array(
                'form' => $form->createView(),
                'error' => null,
                'title' => $varTitle,
            ));
        } else {
            return $this->render('passwordbox/index.html.twig', array(
                'form' => $form->createView(),
                'error' => null,
                'title' => $varTitle,
            ));
        }
    }

    
    #[Route("/{_locale}/{slug}",
          name: "timezonepage",
          requirements: ["slug" => "timezone"],
          defaults: ["edit" => null]
      )]
    #[Route("/{_locale}/{slug}/{edit}",
          name: "timezoneeditpage",
          requirements: ["slug" => "timezone", "edit" => "edit"]
      )]
    public function timezoneAction(Request $request, $slug, $edit, SessionInterface $session)
    {
        $task = new eFaInitTask();

        $varData = $session->get($slug);
        
        if ($edit === 'edit') {
            $form = $this->createForm(TimezoneEditTaskType::class, $task, array('varData' => $varData));
        } else { 
            $form = $this->createForm(TimezoneTaskType::class, $task, array('varData' => $varData));
        }
    
        $form->handleRequest($request);
    
        if ($form->isSubmitted() && $form->isValid()) {
            $task = $form->getData();

            $session->set('timezone', $task->getTimezone()); 
            
            if ($edit === 'edit') {
                $action = 'verify';
                $page   = 'verifysettingspage';
            } else {
                $action = $form->get('Next')->isClicked() || $form->get('NextHidden')->isClicked() ? 'mailserver' : 'configutc';
                $page   = $form->get('Next')->isClicked() || $form->get('NextHidden')->isClicked() ? 'textboxpage' : 'yesnopage';
            }

            return $this->redirectToRoute($page, array('_locale' => $request->getLocale(), 'slug' => $action));
        }

        if ($edit === 'edit') {
            return $this->render('timezoneedit/index.html.twig', array(
                'form' => $form->createView(),
                'title' => 'Timezone Selection'
            ));
        } else {
            return $this->render('timezone/index.html.twig', array(
                'form' => $form->createView(),
                'title' => 'Timezone Selection'
            ));
        }
    }

    #[Route("/{_locale}/{slug}",
          name: "verifysettingspage",
          requirements: ["slug" => "verify"],
      )]
    public function verifySettingsAction(Request $request, $slug, SessionInterface $session)
    {
        $task = new eFaInitTask();

        $form = $this->createForm(VerifySettingsTaskType::class, $task);

        $form->handleRequest($request);

        $ipv4addressflag=false;
        $ipv4netmaskflag=false;
        $ipv4gatewayflag=false;
        $ipv6addressflag=false;
        $ipv6prefixflag=false;
        $ipv6gatewayflag=false;
        $dns1flag=false;
        $dns2flag=false;
        $errormessage='';

        if ($form->isSubmitted() && $form->isValid()) {
            $task = $form->getData();

            $isValid=true;

            // Verify setting groups for sanity and completeness, highlight in red any that need attention
            if ($session->get('configipv4') === '1') {
                if ($session->get('ipv4address') == '') {
                    $isValid=false;
                    $ipv4addressflag=true;
                }
                if ($session->get('ipv4netmask') == '') {
                    $isValid=false;
                    $ipv4netmaskflag=true;
                }
                if ($session->get('ipv4gateway') == '') {
                    $isValid=false;
                    $ipv4gatewayflag=true;
                }
            } 
            if ($session->get('configipv6') === '1') {
                if ($session->get('ipv6address') == '') {
                    $isValid=false;
                    $ipv6addressflag=true;
                }
                if ($session->get('ipv6prefix') == '') {
                    $isValid=false;
                    $ipv6prefixflag=true;
                }
                if ($session->get('ipv6gateway') == '') {
                    $isValid=false;
                    $ipv6gatewayflag=true;
                }
            } 

            if ($session->get('configrecursion') === '0') {
                if ($session->get('dns1') == '') {
                    $isValid=false;
                    $dns1flag=true;
                }
                if ($session->get('dns2') == '') {
                    $isValid=false;
                    $dns2flag=true;
                }
            } 

            if ($isValid === true) {
                $output = '<br/>eFa -- Starting and Configuring MariaDB...<br/>';

                $session->set('output', $output);

                return $this->render('configure/index.html.twig', array(
                    'title'      => "Configuring",
                    'output'     => $output,
                    'progress'   => "0",
		            'next'       => "configuredo1"
                ));
            } else {
               $errormessage = 'Please fix the items above before continuing.';
            }
        }

        return $this->render('verifysettings/index.html.twig', array(
            'form'            => $form->createView(),
            'title'           => 'Verify Settings',
            'language'        => $session->get('locale'),
            'hostname'        => $session->get('hostname'),
            'domainname'      => $session->get('domainname'),
            'email'           => $session->get('email'),
            'interface'       => $session->get('interface'),
            'configipv4'      => $session->get('configipv4'),
            'ipv4address'     => $session->get('ipv4address'), 'ipv4addressflag' => $ipv4addressflag,
            'ipv4netmask'     => $session->get('ipv4netmask'), 'ipv4netmaskflag' => $ipv4netmaskflag,
            'ipv4gateway'     => $session->get('ipv4gateway'), 'ipv4gatewayflag' => $ipv4gatewayflag,
            'configipv6'      => $session->get('configipv6'),
            'ipv6address'     => $session->get('ipv6address'), 'ipv6addressflag' => $ipv6addressflag,
            'ipv6prefix'      => $session->get('ipv6prefix'),  'ipv6prefixflag'  => $ipv6prefixflag,
            'ipv6gateway'     => $session->get('ipv6gateway'), 'ipv6gatewayflag' => $ipv6gatewayflag,
            'configrecursion' => $session->get('configrecursion'),
            'dns1'            => $session->get('dns1'), 'dns1flag' => $dns1flag,
            'dns2'            => $session->get('dns2'), 'dns2flag' => $dns2flag,
            'webusername'     => $session->get('webusername'),
            'cliusername'     => $session->get('cliusername'),
            'configvirtual'   => $session->get('configvirtual'),
            'configutc'       => $session->get('configutc'),
            'timezone'        => $session->get('timezone'),
            'mailserver'      => $session->get('mailserver'),
            'orgname'         => $session->get('orgname'),
            'errormessage'    => $errormessage,
        ));
    }

    #[Route("{_locale}/configuredo1")]
    public function eFaConfigure(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        // Start MariaDB
        $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--startmariadb']);

        try {
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Started and Configured MariaDB<br/>' . $output;

            $output = '<br/>eFa -- Configuring host and domain...<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error starting and configuring MariaDB"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "4",
		    'next'       => "configuredo2"
        ));
    }

    #[Route("{_locale}/configuredo2")]
    public function eFaConfigure2(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        $process = new Process(['sudo', '/usr/sbin/eFa-Commit' ,'--confighost', '--ipv4address=' . $session->get('ipv4address'), '--hostname=' . $session->get('hostname'), '--domainname=' . $session->get('domainname'), '--ipv6address=' . $session->get('ipv6address')]);

        try {
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Configured host and domain<br/>' . $output;

            $output = '<br/>eFa -- Configuring DNS...<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring host and domain"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "8",
		    'next'       => "configuredo3"
        ));
    }

    #[Route("{_locale}/configuredo3")]
    public function eFaConfigure3(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configdns', '--ipv6dns=' . $session->get('ipv6dns'), '--enablerecursion=' . $session->get('configrecursion'), '--dnsip1=' . $session->get('dns1'), '--dnsip2=' . $session->get('dns2')]);

        try {
            $process->setTimeout($this->timeout);
            $process->mustRun();
            
            $output = '<br/> eFa -- DNS Configured<br/>' . $output;

            $output = '<br/>eFa -- Configuring interface...<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring DNS"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "12",
		    'next'       => "configuredo4"
        ));
    }

    #[Route("{_locale}/configuredo4")]
    public function eFaConfigure4(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configip', '--interface=' . $session->get('interface'), '--ipv4address=' . $session->get('ipv4address'), '--ipv4netmask=' . $session->get('ipv4netmask'), '--ipv4gateway=' . $session->get('ipv4gateway'), '--ipv6address=' . $session->get('ipv6address'), '--ipv6mask=' . $session->get('ipv6prefix'), '--ipv6gateway=' . $session->get('ipv6gateway'), '--dnsip1=' . $session->get('dns1'), '--dnsip2=' . $session->get('dns2')]);

        try {
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Interface configured<br/>' . $output;

            $output = '<br/>eFa -- Generating host keys (this may take a while)...<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring interface"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "16",
		    'next'       => "configuredo5"
        ));
    }

    #[Route("{_locale}/configuredo5")]
    public function eFaConfigure5(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--genhostkeys']);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/>eFa -- Generated host keys<br/>' . $output;

            $output = '<br/>eFa -- Configuring Timezone<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error generating host keys"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "20",
		    'next'       => "configuredo6"
        ));
    }

    #[Route("{_locale}/configuredo6")]
    public function eFaConfigure6(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configtzone', '--timezone=' . $session->get('timezone'), '--isutc=' . $session->get('configutc')]);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Timezone configured<br/>' . $output;

            $output = '<br/>eFa -- Configuring razor<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error setting timezone"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "24",
		    'next'       => "configuredo7"
        ));
    }

    #[Route("{_locale}/configuredo7")]
    public function eFaConfigure7(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configrazor']);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Configured razor<br/>' . $output;

            $output = '<br/>eFa -- Configure transport<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring razor"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "28",
		    'next'       => "configuredo8"
        ));
    }

    #[Route("{_locale}/configuredo8")]
    public function eFaConfigure8(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configtransport', '--hostname=' . $session->get('hostname'), '--domainname=' . $session->get('domainname'), '--mailserver=' . $session->get('mailserver'), '--adminemail=' . $session->get('email')]);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Transport configured<br/>' . $output;

            $output = '<br/>eFa -- Configuring Spamassassin<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring transport"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "32",
		    'next'       => "configuredo9"
        ));
    }

    #[Route("{_locale}/configuredo9")]
    public function eFaConfigure9(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configsa', '--orgname=' . $session->get('orgname')]);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Spamassassin configured<br/>' . $output;

            $output = '<br/>eFa -- Configuring MailScanner<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring spamassassin"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "36",
		    'next'       => "configuredo10"
        ));
    }

    #[Route("{_locale}/configuredo10")]
    public function eFaConfigure10(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configmailscanner', '--orgname=' . $session->get('orgname'), '--adminemail=' . $session->get('email'), '--hostname=' . $session->get('hostname'), '--domainname=' . $session->get('domainname')]);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- MailScanner configured<br/>' . $output;

            $output = '<br/>eFa -- Configuring MailWatch<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring mailscanner"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "40",
		    'next'       => "configuredo11"
        ));
    }

    #[Route("{_locale}/configuredo11")]
    public function eFaConfigure11(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $password = $session->get('webpassword');
            # Hash the password now
            $password = password_hash($password, PASSWORD_DEFAULT);
            $process = Process::fromShellCommandline("sudo /usr/sbin/eFa-Commit --configmailwatch --hostname=" . $session->get('hostname') . " --domainname=" . $session->get('domainname') . " --timezone=" . $session->get('timezone') . " --username=" . $session->get('webusername') . " --efauserpwd='" . $password . "'");
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- MailWatch configured<br/>' . $output;

            $output = '<br/>eFa -- Configuring SASL<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring MailWatch"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "44",
		    'next'       => "configuredo12"
        ));
    }

    #[Route("{_locale}/configuredo12")]
    public function eFaConfigure12(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configsasl']);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- SASL configured<br/>' . $output;

            $output = '<br/>eFa -- Configuring SQLGrey<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring SASL"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "48",
		    'next'       => "configuredo13"
        ));
    }

    #[Route("{_locale}/configuredo13")]
    public function eFaConfigure13(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configsqlgrey']);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- SQLGrey configured<br/>' . $output;

            $output = '<br/>eFa -- Configuring openDMARC<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring SQLGrey"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "52",
		    'next'       => "configuredo14"
        ));
    }

    #[Route("{_locale}/configuredo14")]
    public function eFaConfigure14(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configdmarc']);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- openDMARC configured<br/>' . $output;

            $output = '<br/>eFa -- Configuring apache<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring openDMARC"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "56",
		    'next'       => "configuredo15"
        ));
    }

    #[Route("{_locale}/configuredo15")]
    public function eFaConfigure15(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configapache', '--adminemail=' . $session->get('email'), '--hostname=' . $session->get('hostname'), '--domainname=' . $session->get('domainname')]);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Apache configured<br/>' . $output;

            $output = '<br/>eFa -- Configuring dnf-automatic<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring Apache"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "60",
		    'next'       => "configuredo16"
        ));
    }

    #[Route("{_locale}/configuredo16")]
    public function eFaConfigure16(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configyumcron', '--hostname=' . $session->get('hostname'), '--domainname=' . $session->get('domainname'), '--adminemail=' . $session->get('email')]);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- dnf-automatic configured<br/>' . $output;

            $output = '<br/>eFa -- Locking down root<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring...error",
                'output'     => $output,
                'error'      => "Error configuring dnf-automatic"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "64",
		    'next'       => "configuredo17"
        ));
    }

    #[Route("{_locale}/configuredo17")]
    public function eFaConfigure17(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configroot']);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Root locked down<br/>' . $output;

            $output = '<br/>eFa -- Configuring CLI<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error locking down root"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "68",
		    'next'       => "configuredo18"
        ));
    }

    #[Route("{_locale}/configuredo18")]
    public function eFaConfigure18(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $password = $session->get('clipassword');
            $password = exec("python3 -c \"import crypt; print(crypt.crypt('" . $password . "', crypt.mksalt(crypt.METHOD_SHA512)))\"");
            $process = Process::fromShellCommandline("sudo /usr/sbin/eFa-Commit --configcli --cliusername=" .  $session->get('cliusername') . " --efaclipwd='" . $password . "'");
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Configured CLI<br/>' . $output;

            $output = '<br/>eFa -- Configuring self-signed cert<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring CLI"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "72",
		    'next'       => "configuredo19"
        ));
    }

    #[Route("{_locale}/configuredo19")]
    public function eFaConfigure19(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configcert', '--hostname=' . $session->get('hostname'), '--domainname=' . $session->get('domainname')]);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Configured self-signed cert<br/>' . $output;

            $output = '<br/>eFa -- Locking down mysql <br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error configuring self-signed cert"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "76",
		    'next'       => "configuredo20"
        ));
    }

    #[Route("{_locale}/configuredo20")]
    public function eFaConfigure20(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--configmysql']);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Locked down mysql<br/>' . $output;

            $output = '<br/>eFa -- Finalizing configuration and rebooting <br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error locking down mysql"
            ));
        }

        $session->set('output', $output);

        return $this->render('configure/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output,
            'progress'   => "80",
		    'next'       => "configuredo21"
        ));
    }

    #[Route("{_locale}/configuredo21")]
    public function eFaConfigure21(Request $request, SessionInterface $session) 
    {
        $output = $session->get('output');

        if ( $session->get('ipv4address') != '' || $session->get('ipvtaddress') != '') {
            $buffer = '<br/>eFa -- Please visit after reboot is complete (in a few minutes):<br/><br/>';      
        }
        if ( $session->get('ipv4address') != '' ) {
            $buffer .= '<a href="https://' . $session->get('ipv4address') . '/mailscanner">https://' . $session->get('ipv4address') . '/mailscanner</a><br/><br/>';
        }
        if ( $session->get('ipv6address') != '' ) {
            $buffer .= '<a href="https://' . $session->get('ipv6address') . '/mailscanner">https://' . $session->get('ipv6address') . '/mailscanner</a><br/><br/>';
        }

        $output = $buffer . $output;

        try {
            $process = new Process(['sudo', '/usr/sbin/eFa-Commit', '--finalize', '--configvirtual=' .  $session->get('configvirtual')]);
            $process->setTimeout($this->timeout);
            $process->mustRun();

            $output = '<br/> eFa -- Configuration complete, preparing to reboot in 60 seconds!<br/>' . $output;

        } catch (ProcessFailedException $exception) {
            return $this->render('configureerror/index.html.twig', array(
                'title'      => "Configuring",
                'output'     => $output,
                'error'      => "Error finalizing configuration"
            ));
        }

        return $this->render('configuredone/index.html.twig', array(
            'title'      => "Configuring",
            'output'     => $output
        ));
    }
}
?>
