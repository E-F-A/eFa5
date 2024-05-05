<?php
// tests/Controller/eFaInitControllerTest.php
namespace App\Tests\Controller;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

class eFaInitControllerTest extends WebTestCase
{
    public function testWelcomeEn(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/en');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Welcome to eFa');
    }
    public function testWelcomeCz(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/cz');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Vítejte v eFa');
    }
    public function testWelcomeDa(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/da');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Velkommen til eFa');
    }
    public function testWelcomeNl(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/nl');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Welkom bij eFa');
    }
    public function testWelcomeFr(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/fr');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Bienvenue dans eFa');
    }
    public function testWelcomeDe(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/de');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Willkommen bei eFa');
    }
    public function testWelcomeEl(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/el');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Καλώς ήρθατε στο eFa');
    }
    public function testWelcomeIt(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/it');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Benvenuto su eFa');
    }
    public function testWelcomeNo(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/no');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Velkommen til eFa');
    }
    public function testWelcomePt(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/pt_PT');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Bem-vindo a(o) eFa');
    }
    public function testWelcomeRu(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/ru');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Добро пожаловать в eFa');
    }
    public function testWelcomeZh_CN(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/zh_CN');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', '欢迎 eFa');
    }
    public function testWelcomeSv(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/sv');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Välkommen till eFa');
    }
    public function testWelcomezh_TW(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/zh_TW');

        $this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', '歡迎 eFa');
    }
    public function testWelcomeNext(): void
    {
        $client = static::createClient();
        $crawler = $client->request('GET', '/en');
    
	$client->followRedirects();
	$crawler = $client->submitForm('Next');
	
	$this->assertResponseIsSuccessful();
        $this->assertSelectorTextContains('h1', 'Hostname');
	
    }
}
